from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from models import Post
import json
import random
from django.http import HttpResponseRedirect
from datetime import datetime
# Create your views here.


class PostAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'post.html')
    
    def post(self, request, *args, **kwargs):
        body = json.loads(self.request.body)
        full_comment = body['comment']
        hidden_comment  = full_comment[:max(16,int(.2*len(full_comment)))] + "..."
        Post.objects.create(
            company=body['company'], 
            position=body['position'],
            hidden_comment=hidden_comment,
            full_comment=full_comment, 
            score=random.randint(0,100),
            sub_date=datetime.utcnow())
        return HttpResponseRedirect('/')

class Reveal(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(Post.objects.get(id=request.GET['id']).full_comment)