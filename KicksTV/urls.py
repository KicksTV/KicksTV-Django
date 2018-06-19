from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

from .forms import UserProfileRegistrationForm

from . import views
import gallery
import kickstvDropbox
import blog
import userProfile




urlpatterns = [
    # Home Page Url
    url(r'^$', views.index, name="index"),
    url(r'^admin/', admin.site.urls),
    
    # Dropbox Urls
    url(r'^dropbox/', include('kickstvDropbox.urls', namespace='dropbox')),
    
    # Blog Urls
    url(r'^blog/', include('blog.urls', namespace='blogs')),
    
    # UserProfile Urls
    url(r'^(?P<user>[\w-]+)/profile/', include('userProfile.urls', namespace='profile')),
    
    # Gallery Urls
    url(r'^gallery/(?P<gallery_user>[\w-]+)/', include('gallery.urls', namespace='gallerys')),
    url(r'^featured/gallerys$', gallery.views.featuredGallery, name='featured-gallery'),
    url(r'^search/gallerys', gallery.views.searchGallery, name='search-gallery'),
	url(r'^search/gallery/result$', gallery.views.GallerySearchListView.as_view(), name='gallery-search-list-view'),

    # Custom Registration Redux Registration 
    url(r'^accounts/register$', views.MyRegistrationView.as_view(), name="registration_register"),

    # Registration Redux Urls
    url(r'^accounts/', include('registration.backends.default.urls')),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
