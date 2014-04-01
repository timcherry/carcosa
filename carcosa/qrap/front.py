from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, Template
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from models import Post
from django.template import RequestContext, loader

class Front(View):
    def get(self, request, *args, **kwargs):
        sorted_posts = sorted(Post.objects.all(), key=lambda x: x.score, reverse=True)
        return render(request, 'index.html', {"posts":sorted_posts})
