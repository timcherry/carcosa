from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, Template
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from models import Post
from django.template import RequestContext, loader
from datetime import datetime
import redis
import json

redis_c = redis.StrictRedis(host='localhost', port=6379, db=0)

SSET_KEY = "popular"

def render_list_of_posts(ids):
    posts = []
    for id in ids:
        try:
            post = Post.objects.get(id=id)
            post.pretty_date = get_pretty_date(post.sub_date)
            posts.append(post)
        except Exception as e:
            print "ID MISMATCH. ID:%s NOT FOUND IN MONGODB. Error:%s"%(id, e)
            continue
    return posts

def get_pretty_date(date):
    diff =  datetime.utcnow() - date
    if diff.days:
        mag = diff.days
        unit = "days" if mag > 1 else "days"
    elif diff.seconds >= 60*60:
        mag = diff.seconds/60/60
        unit = "hours" if mag > 1 else "hour"
    elif diff.seconds >= 60:
        mag = diff.seconds/60
        unit = "minutes" if mag > 1 else "minute"
    else:
        mag = diff.seconds
        unit = "seconds" if mag > 1 else "second"
    return "Submitted %s %s ago"%(mag,unit)


def build_ios_dict(posts):
    ret_posts = []
    for post in posts:
        ret_posts.append({"hidden_comment": post.hidden_comment})
    return ret_posts

class HotList(View):
    def get(self, request, *args, **kwargs):
        posts = render_list_of_posts(redis_c.zrange(SSET_KEY, 0, -1, desc=True))
        ios_posts = build_ios_dict(posts)
        return HttpResponse(json.dumps(ios_posts))

class AutoComplete(View):
    def get(self, request, *args, **kwargs):
        suggestions = ["fooz", "booz", "baaaaaz"]
        return HttpResponse(json.dumps(suggestions))
