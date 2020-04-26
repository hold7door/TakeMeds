from django.conf.urls import include,url

from . import views

app_name = 'location'

urlpatterns = [
    url(r'^$',views.location,name='location'),
]
