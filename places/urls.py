from django.conf.urls import include,url
from . import views

app_name = 'places'

urlpatterns = [
    url(r'^$',views.search_results,name = 'search_results'),
]
