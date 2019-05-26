

from datetime import datetime

from django.shortcuts import render

def index(request):
    return render(request , 'takemeds/index.html',context={'user':request.user})	
