from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.moduleView, name='modules'),
	url(r'^module/create', views.createModule, name="module-create"),
	url(r'^(?P<module_id>[0-9]+)/delete$', views.deleteModule, name="module-delete"),

	url(r'^module/(?P<module_id>[0-9]+)/$', views.courseWorkView, name="courseWork"),
	url(r'^(?P<module_id>[0-9]+)/coursework/create', views.createCourseWork, name="courseWork-create"),
	url(r'^(?P<folder>)', views.folderView, name="folderView"),
]