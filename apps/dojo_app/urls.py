from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^validate/$', views.validate),
    url(r'^login/$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^secrets$', views.popular_secrets),
    url(r'^secrets/create$', views.create_secret),
    url(r'^secrets/(?P<id>\d+)/like$', views.like),
    url(r'^secrets/(?P<id>\d+)/delete$', views.delete),
    url(r'^logout$', views.logout)
]
