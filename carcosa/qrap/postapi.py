from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from models import Post
import json
import random
from django.http import HttpResponseRedirect
# Create your views here.


class PostAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'post.html')
    
    def post(self, request, *args, **kwargs):
        body = json.loads(self.request.body)
        Post.objects.create(
            company=body['company'], 
            position=body['position'], 
            comment=body['comment'], 
            score=random.randint(0,100))
        #import pdb; pdb.set_trace()
        return HttpResponseRedirect('/')