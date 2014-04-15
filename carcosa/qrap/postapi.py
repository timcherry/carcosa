from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from models import Post
import json
import random
from django.http import HttpResponseRedirect
from datetime import datetime
import redis
import oauth2 as oauth
import httplib2
import time, os, simplejson
import requests

SSET_KEY = "popular"

consumer_key      =   '75yk9z2ug0z54w'
consumer_secret  =   'iGZx5JiRnkVJWYxn'
user_token           =   '14c8d65a-ef5d-4eff-b93d-72caf3c0020d'
user_secret          =   '867c6833-0886-4991-85c9-ee91f2205b11'
 

consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)

class PostAPI(View):
    redis_c = redis.StrictRedis(host='localhost', port=6379, db=0)
    oauth_url = "https://www.linkedin.com/uas/oauth2/accessToken?grant_type=authorization_code&code=%s&redirect_uri=%s&client_id=%s&client_secret=%s"

    
    def get(self, request, *args, **kwargs):
        url = self.oauth_url%(request.GET['code'], "http://localhost:8000/post", "75yk9z2ug0z54w", "iGZx5JiRnkVJWYxn")
        resp = requests.post( url)
        resp_json = resp.json()
        access_token = resp_json['access_token']
        expires_in = resp_json['expires_in']
        url_positions = "https://api.linkedin.com/v1/people/~/positions?oauth2_access_token=%s"%(access_token)
        resp_pos = requests.get(url_positions, headers={'x-li-format': 'json'})
        all_positions = resp_pos.json()['values']
        # parse current position
        cur_postion= all_positions.pop(0)
        cur_company_name = cur_postion["company"]["name"]
        cur_company_title = cur_postion["title"]
        titles = []
        companies = []
        for postion in all_positions:
            titles.append(postion["title"])
            companies.append(postion["company"]["name"])
        return render(request, 'post.html', {'cur_company_name': cur_company_name, 'cur_company_title': cur_company_title, 'companies':companies, 'titles': titles} )
    
    def post(self, request, *args, **kwargs):
        body = json.loads(self.request.body)
        full_comment = body['comment']
        hidden_comment  = full_comment[:max(16, int(.2*len(full_comment)))] + "..."
        px = Post.objects.create(
            company=body['company'], 
            position=body['position'],
            hidden_comment=hidden_comment,
            full_comment=full_comment, 
            sub_date=datetime.utcnow())
        rand_start_score = random.randint(1, 100)
        self.redis_c.zincrby(SSET_KEY, px.id, rand_start_score)
        self.redis_c.zincrby(SSET_KEY + "-" + px.company , px.id, rand_start_score)

        return HttpResponseRedirect('/')

class Reveal(View):
    redis_c = redis.StrictRedis(host='localhost', port=6379, db=0)
    def get(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.GET['id'])
        self.incr_score(post, 1)
        return HttpResponse(post.full_comment)

    def incr_score(self, post, count=1):
        self.redis_c.zincrby(SSET_KEY, post.id, count)
        self.redis_c.zincrby(SSET_KEY + "-" + post.company , post.id, count)
