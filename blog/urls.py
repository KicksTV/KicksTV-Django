from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    
    url(r'^(?P<slug>[\w-]+)/$', views.projectDetailView, name="project-detail"),
    url(r'^add/$', views.projectAddView, name="project-add"),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.projectDeleteView, name="project-delete"),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.projectEditView, name="project-edit"),


    url(r'^(?P<slug>[\w-]+)/post/(?P<post_id>[0-9]+)/$', views.blogDetailView, name="post-detail"),
    url(r'^(?P<slug>[\w-]+)/post/add/$', views.blogAddView, name="post-add"),
    url(r'^(?P<slug>[\w-]+)/post/(?P<post_id>[0-9]+)/delete/$', views.blogDeleteView, name="post-delete"),
    url(r'^(?P<slug>[\w-]+)/post/(?P<post_id>[0-9]+)/edit/$', views.blogEditView, name="post-edit"),
]