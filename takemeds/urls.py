from django.conf.urls import include,url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from . import views
import accounts
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^search/',include('places.urls')),
    url(r'^loc/',include('location.urls')),
    url(r'^login/',include('accounts.urls')),
    url(r'^logout$',accounts.views.logout_request,name='logout_request'),
]
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)