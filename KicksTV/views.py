import requests, json
from django.conf import settings

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Permission, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from gallery.models import Gallery, Image, User
from blog.models import Post, Project

def index(request):
	gallery = Gallery.objects.filter(is_homepage_gallery=True)
	desktop_gallery = None
	mobile_gallery = None

	for g in gallery:
		if g.gallery_title == "Home Page Desktop Gallery":
			desktop_gallery = g
		elif g.gallery_title == "Home Page Mobile Gallery":
			mobile_gallery = g

	
	
	url = "http://mcapi.de/api/server-query/mc.vanillahigh.net/25565"
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
	result = requests.get(url, headers=headers)
	results = result.content.decode()
	data = json.loads(results)


	user = User.objects.get(username="kickstv")
	all_projects = Project.objects.filter(user=user)

	paginator = Paginator(all_projects, 6) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		project = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		project = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		project = paginator.page(paginator.num_pages)




	context = {
		'all_projects': project,
		'desktop_gallery': desktop_gallery,
		'mobile_gallery': mobile_gallery,
		'serverStatus': data['result']['status'],
		'hostname': data['hostname'],
		'onlinePlayers': data['players']['online'],
		'maxPlayers': data['players']['max'],
		'list': data['players']['list'],
		}
	return render(request, "index.html", context)