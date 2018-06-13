from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.galleryView, name='index'),
	url(r'^(?P<slug>[\w-]+)/$', views.detailView, name="detail"),
	url(r'^gallery/add/$', views.galleryCreate, name="gallery-add"),
	url(r'^gallery/(?P<slug>[\w-]+)/$', views.galleryUpdate, name="gallery-update"),
	url(r'^gallery/(?P<slug>[\w-]+)/delete/$', views.galleryDelete, name="gallery-delete"),
	url(r'^gallery/(?P<slug>[\w-]+)/favorite/$', views.galleryFavorite, name="favorite"),

	url(r'^(?P<slug>[\w-]+)/image/add/$', views.imageCreate, name='image-add'),
	url(r'^(?P<slug>[\w-]+)/delete/image/(?P<image_id>[0-9]+)/$', views.imageDelete, name='image-delete'),
	]