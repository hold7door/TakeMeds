from django.conf.urls import include,url

from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^$',views.login_page,name='login_page'),
    url(r'^submit$',views.login_request,name='login_request'),
    url(r'^createnew$',views.create_request,name='create_request'),
    url(r'^changepass$',views.change_pass,name='change_pass'),
]
