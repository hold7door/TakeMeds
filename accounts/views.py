# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

# Create your views here.

def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    return render(request , 'accounts/login_form.html')

	
def login_request(request):
    username = request.POST['username']
    password = request.POST['passwd']
    user = authenticate(request , username = username, password=password)
    if user is not None:
        login(request,user)
        return HttpResponseRedirect('/')
    else:
        return render(request,'accounts/login_form.html')
def logout_request(request):
    logout(request)
    return HttpResponseRedirect('/')
	
	
def create_request(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        return render(request,'accounts/create_form.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['passwd']
        email = request.POST['email']
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return HttpResponse('Username already Exists')
        return HttpResponseRedirect('/')
		
def change_pass(request):
    pass
