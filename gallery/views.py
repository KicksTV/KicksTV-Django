import operator
from django.views.generic import ListView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import GalleryForm, ImageForm
from .models import Gallery, Image, User

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# Create your views here.

def userGalleryView(request, gallery_user):
	gallery_user = get_object_or_404(User, username=gallery_user)
	all_gallery = Gallery.objects.filter(user=gallery_user).order_by("-gallery_date")

	paginator = Paginator(all_gallery, 9)
	page = request.GET.get('page')
	try:
		gallery = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		gallery = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		gallery = paginator.page(paginator.num_pages)
	
	return render(request, 'gallery/user_gallery.html', {
		'all_gallery': gallery,
		'user': gallery_user,
		})
			



def userDetailView(request, gallery_user, slug):
	user = get_object_or_404(User, username=gallery_user)
	gallery = get_object_or_404(Gallery, slug=slug)
	
	context = {
		'user': user,
		'gallery': gallery,
	}
	return render(request, 'gallery/user_gallery_detail.html', context)




def galleryCreate(request, gallery_user):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	else:
		form = GalleryForm(request.POST or None, request.FILES or None)
		if form.is_valid():
		    gallery = form.save(commit=False)
		    gallery.user = request.user
		    gallery.gallery_image = request.FILES['gallery_image']
		    file_type = gallery.gallery_image.url.split('.')[-1]
		    file_type = file_type.lower()
		    if file_type not in IMAGE_FILE_TYPES:
		        context = {
		            'formTitle': 'Create Gallery',
		            'gallery': gallery,
		            'form': form,
		            'error_message': 'Image file must be PNG, JPG, or JPEG',
		        }
		        return render(request, 'default-form.html', context)
		    gallery.save()
		    messages.success(request, "Successfully Created!")
		    return HttpResponseRedirect(gallery.get_absolute_url())
		context = {
		    'formTitle': 'Create Gallery',
		    'form': form,
		}
		return render(request, 'default-form.html', context)

def galleryUpdate(request, gallery_user, slug):
	gallery = get_object_or_404(Gallery, slug=slug)
	form = GalleryForm(request.POST or None, instance=gallery)
	if form.is_valid():
		gallery = form.save(commit=False)
		try:
			gallery.gallery_image = request.FILES['gallery_image']
			file_type = gallery.gallery_image.url.split('.')[-1]
			file_type = file_type.lower()
			if file_type not in IMAGE_FILE_TYPES:
				context = {
					'formTitle': 'Update Gallery',
					'gallery': gallery,
					'form': form,
					'error_message': 'Image file must be PNG, JPG, or JPEG',
					}
				return render(request, 'default-form.html', context)
		except MultiValueDictKeyError:
			gallery.gallery_image = gallery.gallery_image

		form.save()
		messages.success(request, "Successfully Editted!")
		return HttpResponseRedirect(gallery.get_absolute_url())
	context = {
		'formTitle': 'Update Gallery',
		'form': form,
	}
	return render(request, 'default-form.html', context)

def galleryDelete(request, gallery_user, slug):
	gallery = get_object_or_404(Gallery, slug=slug)
	gallery.delete()
	messages.error(request, "Successfully Deleted!")
	return HttpResponseRedirect(reverse('gallerys:user-gallery', args=[gallery_user]))


def imageCreate(request, gallery_user, slug):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	else:
		form = ImageForm(request.POST or None, request.FILES or None)
		gallery = get_object_or_404(Gallery, slug=slug)
		if form.is_valid():
		    image = form.save(commit=False)
		    image.gallery = gallery
		   
		    image.image_image = request.FILES['image_image']
		    file_type = gallery.gallery_image.url.split('.')[-1]
		    file_type = file_type.lower()
		    if file_type not in IMAGE_FILE_TYPES:
		        context = {
		            'formTitle': 'Add Image',
		            'image': image,
		            'form': form,
		            'error_message': 'Image file must be PNG, JPG, or JPEG',
		        }
		        return render(request, 'default-form.html', context)
		    image.save()
		    messages.success(request, "Successfully Added!")
		    return HttpResponseRedirect(gallery.get_absolute_url())
		context = {
		    'formTitle': 'Add Image',
		    "form": form,
		}
		return render(request, 'default-form.html', context)


def imageDelete(request, gallery_user, slug, image_id):
	gallery = get_object_or_404(Gallery, slug=slug)
	image = get_object_or_404(Image, pk=image_id)
	image.delete()
	messages.error(request, "Successfully Deleted!")
	return HttpResponseRedirect(gallery.get_absolute_url())

def featuredGallery(request):
	all_gallery = Gallery.objects.filter(is_favorite=True)
	if all_gallery:
		return render(request, 'gallery/featured.html', {'object_list': all_gallery})
	else:
		return render(request, 'gallery/noFeatured.html')


def galleryFavorite(request, gallery_user, slug):
	all_gallery = Gallery.objects.all()
	gallery = get_object_or_404(Gallery, slug=slug)
	try:
		if gallery.is_favorite:
			gallery.is_favorite = False
		else:
			gallery.is_favorite = True

		gallery.save()
	except (KeyError, Gallery.DoesNotExist):
		return HttpResponse("<h1>Gallery Does Not Exist!</h1>")
	else:
		messages.success(request, "Successfully Featured!")
		return HttpResponseRedirect(reverse('featured-gallery'))

def searchGallery(request):
	return render(request, 'gallery/search-gallery.html')


class GallerySearchListView(ListView):
    model = Gallery
    template_name = 'gallery/search-gallery.html'
    paginate_by = 10

    def get_queryset(self):
        all_gallery = Gallery.objects.all()
        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            vectors = SearchVector('gallery_title')
            all_gallery = all_gallery.annotate(search=vectors).filter(search=query)
        return all_gallery
