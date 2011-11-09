from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from nut import urls as nut_urls

urlpatterns = patterns('',
    url(r'', include(nut_urls)),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
