from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

from . import views
import gallery
import kickstvDropbox
import blog
import userProfile

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^admin/', admin.site.urls),
    url(r'^gallery/(?P<gallery_user>[\w-]+)/', include('gallery.urls', namespace='gallerys')),
    url(r'^dropbox/', include('kickstvDropbox.urls', namespace='dropbox')),
    url(r'^blog/', include('blog.urls', namespace='blogs')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    
    url(r'^featured/gallerys$', gallery.views.featuredGallery, name='featured-gallery'),
    url(r'^search/gallerys', gallery.views.searchGallery, name='search-gallery'),
	url(r'^search/gallery/result$', gallery.views.GallerySearchListView.as_view(), name='gallery-search-list-view'),

    url(r'^(?P<user>[\w-]+)/profile/', include('userProfile.urls', namespace='profile')),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
