from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, Template
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from models import Post
from django.template import RequestContext, loader
import redis

SSET_KEY = "popular"

class Front(View):
    redis_c = redis.StrictRedis(host='localhost', port=6379, db=0)
    MAX_RANGE = -1

    def get(self, request, *args, **kwargs):
        posts = []
        for id in self.redis_c.zrange(SSET_KEY, 0, self.MAX_RANGE, desc=True):
            try:
                posts.append(Post.objects.get(id=id))
            except DoesNotExist, ValidationError:
                print "ID MISMATCH. ID:%s NOT FOUND IN MONGODB"%(id)
                continue
        return render(request, 'index.html', {"posts": posts })
