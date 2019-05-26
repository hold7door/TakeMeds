from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.
def location(request):
    if request.method == "POST":
        request.session['lat'] = request.POST['latitude']
        request.session['lon'] = request.POST['longitude']
        return HttpResponse(json.dumps({"address":"NOT SHOWN"}),content_type="application/json")
