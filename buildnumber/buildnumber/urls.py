from django.conf.urls import include, url

from api import views

urlpatterns = [
    url(r'^api/', include('api.urls')),
]
