from django.conf.urls import url
from django.contrib import messages
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^validate$', views.validate),
    url(r'^login$', views.login), 
    url(r'^dashboard$', views.showall), 
    url(r'^wish_items/(?P<id>\d+)$', views.showitem), 
    url(r'^remove/(?P<id>\d+)$', views.remove), 
    url(r'^delete/(?P<id>\d+)$', views.delete), 
    url(r'^add/(?P<id>\d+)$', views.add), 
    url(r'^create$', views.create),
    url(r'^submit$', views.submit)
]