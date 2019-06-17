from .views import PostView, PostAPIView
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

app_name = 'SocialNetwork'

urlpatterns = [
    url(r'^$', PostAPIView.as_view(), name='post-create'),
    url(r'^(?P<pk>\d+)/$', PostView.as_view(), name='post-read')
]