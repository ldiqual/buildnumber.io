from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^accounts$', views.AccountView.as_view()),
    url(r'^(?P<package_name>.*)/builds$', views.create_build),
    url(r'^(?P<package_name>.*)/builds/(?P<build_number>[0-9]+)$', views.get_build),
    url(r'^(?P<package_name>.*)/builds/last$', views.get_last_build),
]