from django.conf.urls import patterns, url
from BBox.web import views

urlpatterns = patterns('',
    url(r'^$',views.index),
)
