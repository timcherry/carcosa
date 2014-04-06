from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from models import Post
import json
import random
from django.http import HttpResponseRedirect
from datetime import datetime
import redis

SSET_KEY = "popular"


class PostAPI(View):
    redis_c = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    def get(self, request, *args, **kwargs):
        return render(request, 'post.html')
    
    def post(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
        body = json.loads(self.request.body)
        full_comment = body['comment']
        hidden_comment  = full_comment[:max(16,int(.2*len(full_comment)))] + "..."
        px = Post.objects.create(
            company=body['company'], 
            position=body['position'],
            hidden_comment=hidden_comment,
            full_comment=full_comment, 
            sub_date=datetime.utcnow())
        self.redis_c.zadd(SSET_KEY, random.random()*100, px.id)
        return HttpResponseRedirect('/')

class Reveal(View):
    redis_c = redis.StrictRedis(host='localhost', port=6379, db=0)
    def get(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.GET['id'])
        self.incr_score(post.id, 1)
        return HttpResponse(post.full_comment)

    def incr_score(self, id, count=1):
        self.redis_c.zincrby(SSET_KEY, id, count)