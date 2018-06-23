from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.userGalleryView, name="user-gallery"),
	url(r'^view/(?P<slug>[\w-]+)/$', views.userDetailView, name="user-gallery-detail"),
	
	url(r'^add/$', views.galleryCreate, name="gallery-add"),
	url(r'^(?P<slug>[\w-]+)/update$', views.galleryUpdate, name="gallery-update"),
	url(r'^(?P<slug>[\w-]+)/delete/$', views.galleryDelete, name="gallery-delete"),
	url(r'^(?P<slug>[\w-]+)/favorite/$', views.galleryFavorite, name="favorite"),

	url(r'^(?P<slug>[\w-]+)/image/add/$', views.imageCreate, name='image-add'),
	url(r'^(?P<slug>[\w-]+)/delete/image/(?P<image_id>[0-9]+)/$', views.imageDelete, name='image-delete'),
	

	]