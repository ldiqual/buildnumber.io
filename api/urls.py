from django.conf.urls import url

from . import views

# @see https://en.wikipedia.org/wiki/Reverse_domain_name_notation
PACKAGE_REGEX = "[A-Za-z]{2,6}((?!-)\\.[A-Za-z0-9-]{1,63}(?<!-))+"

VERSION_REGEX = "[0-9]+(?:\.[0-9]+)+"

urlpatterns = [
    url(r'^accounts$', views.create_account),
    url(r'^(?P<package_name>%s)/(?P<version>%s/)?builds$' % (PACKAGE_REGEX, VERSION_REGEX), views.create_build),
    url(r'^(?P<package_name>%s)/(?P<version>%s/)?builds/(?P<build_number>[0-9]+)$' % (PACKAGE_REGEX, VERSION_REGEX), views.get_build),
    url(r'^(?P<package_name>%s)/(?P<version>%s/)?builds/last$' % (PACKAGE_REGEX, VERSION_REGEX), views.get_last_build),
]
