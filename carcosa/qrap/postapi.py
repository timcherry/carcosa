from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


class PostAPI(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("BAAAAR")
    
    def post(self, request, *args, **kwargs):
        return HttpResponse(self.request.body)

