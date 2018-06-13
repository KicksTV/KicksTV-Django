from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Permission, User
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Project
from .forms import PostForm, ProjectForm

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
# Create your views here.

def index(request):
	user = User.objects.get(username="kickstv")
	all_projects = Project.objects.filter(user=user).order_by("-timestamp")
	
	
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
	}
	return render(request, 'blog/index.html', context)

def projectDetailView(request, slug):
	project = get_object_or_404(Project, slug=slug)
	all_posts = Post.objects.filter(project=project).order_by("-timestamp")

	paginator = Paginator(all_posts, 10) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		post = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		post = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		post = paginator.page(paginator.num_pages)

	context = {
		'project': project,
		'all_posts': post,
	}
	return render(request, 'blog/projectDetail.html', context)

def projectAddView(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	else:
		form = ProjectForm(request.POST or None, request.FILES or None)
		if form.is_valid():
		    newProject = form.save(commit=False)
		    newProject.image = request.FILES['image']
		    file_type = newProject.image.url.split('.')[-1]
		    file_type = file_type.lower()
		    if file_type not in IMAGE_FILE_TYPES:
		        context = {
		            'newProject': newProject,
		            'form': form,
		            'error_message': 'Image file must be PNG, JPG, or JPEG',
		        }
		        return render(request, 'blog/blog_form.html', context)
		    newProject.save()
		    messages.success(request, 'Successfully Created!')
		    return HttpResponseRedirect(newProject.get_absolute_url())
		context = {
		    "form": form,
		}
	return render(request, 'blog/blog_form.html', context)

def projectDeleteView(request, slug):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	else:
		project = get_object_or_404(Project, slug=slug)
		project.delete()
		messages.error(request, 'Successfully Deleted!')
		return HttpResponseRedirect('/blog')

def projectEditView(request, slug):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	else:
		project = get_object_or_404(Project, slug=slug)
		form = ProjectForm(request.POST or None, request.FILES or None, instance=project)
		if form.is_valid():
		    newProject = form.save(commit=False)
		    try:
			    newProject.image = request.FILES['image']
			    file_type = newProject.image.url.split('.')[-1]
			    file_type = file_type.lower()
			    if file_type not in IMAGE_FILE_TYPES:
			        context = {
			            'newProject': newProject,
			            'form': form,
			            'error_message': 'Image file must be PNG, JPG, or JPEG',
			        }
			        return render(request, 'blog/blog_form.html', context)
		    except MultiValueDictKeyError:
		    	newProject.image = newProject.image
		    	
		    newProject.save()
		    messages.success(request, 'Successfully Eddited!')
		    return HttpResponseRedirect(newProject.get_absolute_url())
		context = {
		    "form": form,
		}
	return render(request, 'blog/blog_form.html', context)

def blogDetailView(request, slug, post_id):
	
	project = get_object_or_404(Project, slug=slug)
	post = get_object_or_404(Post, pk=post_id)

	

	context = {
		'project': project,
		'post': post,
	}
	return render(request, 'blog/postDetail.html', context)



def blogAddView(request, slug):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	else:
		form = PostForm(request.POST or None)
		project = get_object_or_404(Project, slug=slug)
		if form.is_valid():
		    newPost = form.save(commit=False)
		    newPost.project = project
		    newPost.save()
		    messages.success(request, 'Successfully Added!')
		    return HttpResponseRedirect(newPost.get_absolute_url())
		context = {
		    "form": form,
		}
	return render(request, 'blog/blog_form.html', context)



def blogDeleteView(request, slug, post_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	else:
		project = get_object_or_404(Project, slug=slug)
		post = get_object_or_404(Post, pk=post_id)
		post.delete()
		messages.error(request, 'Successfully Deleted!')
		return HttpResponseRedirect(project.get_absolute_url())



def blogEditView(request, slug, post_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	else:
		post = get_object_or_404(Post, id=post_id)
		form = PostForm(request.POST or None, instance=post)
		if form.is_valid():
		    newPost = form.save(commit=False)
		    newPost.save()
		    messages.success(request, 'Successfully Eddited!')
		    return HttpResponseRedirect(newPost.get_absolute_url())
		context = {
		    "form": form,
		}
	return render(request, 'blog/blog_form.html', context)
