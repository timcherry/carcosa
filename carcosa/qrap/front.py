from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, Template
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from models import Post
from django.template import RequestContext, loader
from datetime import datetime

import redis

SSET_KEY = "popular"

class Front(View):
    redis_c = redis.StrictRedis(host='localhost', port=6379, db=0)
    MAX_RANGE = -1

    def get(self, request, *args, **kwargs):
        posts = []
        for id in self.redis_c.zrange(SSET_KEY, 0, self.MAX_RANGE, desc=True):
            try:
                post = Post.objects.get(id=id)
                post.pretty_date = self.get_pretty_date(post.sub_date)
                posts.append(post)
            except:
                print "ID MISMATCH. ID:%s NOT FOUND IN MONGODB"%(id)
                continue
        return render(request, 'index.html', {"posts": posts })

    @classmethod
    def get_pretty_date(cls, date):
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
        return "Submitted %s %s ago."%(mag,unit)
