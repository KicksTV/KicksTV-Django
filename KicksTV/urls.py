from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

from . import views
import gallery
import kickstvDropbox
import blog

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^my_gallery/', include('gallery.urls', namespace='gallerys')),
    url(r'^dropbox/', include('kickstvDropbox.urls', namespace='dropbox')),
    url(r'^featured/', gallery.views.featuredGallery, name='featured'),
    url(r'^blog/', include('blog.urls', namespace='blogs')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', views.index, name="index"),
    
	url(r'^search/gallery/result$', gallery.views.GallerySearchListView.as_view(), name='gallery-search-list-view'),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
