from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.moduleView, name='index'),
	url(r'^file(?P<file>.*)', views.fileDownloadView, name='fileDownload'),
]