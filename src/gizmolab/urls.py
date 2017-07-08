from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from search.views import BookSearchView
from search.forms import BookSearchForm


urlpatterns = patterns('',
                           (r'^', include('textbook.urls')),
                           url(r'^about/',
                               direct_to_template,
                               {'template': 'static/about.html',
                                'extra_context': 
                                    {'default_email': settings.DEFAULT_FROM_EMAIL}},
                               name='about'),
                           (r'^accounts/', include('accounts.urls')),
                           (r'^cart/', include('checkout.urls')),
                           (r'^admin/(.*)', admin.site.root),
                           
                           url(r'^search/$', BookSearchView(form_class=BookSearchForm), name='haystack_search'),
)
