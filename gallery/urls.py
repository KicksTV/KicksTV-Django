from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.userGalleryView, name="user-gallery"),
	url(r'^view/(?P<slug>[\w-]+)/$', views.userDetailView, name="user-gallery-detail"),

	url(r'^my_gallery/$', views.myGalleryView, name='my-gallery'),
	url(r'^my_gallery/view/(?P<slug>[\w-]+)/$', views.myGalleryDetailView, name="my-gallery-detail"),
	url(r'^my_gallery/add/$', views.galleryCreate, name="gallery-add"),
	url(r'^my_gallery/view/(?P<slug>[\w-]+)/update$', views.galleryUpdate, name="gallery-update"),
	url(r'^my_gallery/view/(?P<slug>[\w-]+)/delete/$', views.galleryDelete, name="gallery-delete"),
	url(r'^my_gallery/view/(?P<slug>[\w-]+)/favorite/$', views.galleryFavorite, name="favorite"),

	url(r'^my_gallery/view/(?P<slug>[\w-]+)/image/add/$', views.imageCreate, name='image-add'),
	url(r'^my_gallery/view/(?P<slug>[\w-]+)/delete/image/(?P<image_id>[0-9]+)/$', views.imageDelete, name='image-delete'),
	

	]