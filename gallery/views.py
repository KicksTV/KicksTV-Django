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
def galleryView(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	elif request.user.groups.filter(name='Member').exists():
		all_gallery = Gallery.objects.filter(user=request.user).order_by("-gallery_date")
			
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
		
		return render(request, 'gallery/my_gallery.html', {'all_gallery': gallery})

	else:
		return render(request, 'notMember.html')

			
def detailView(request, slug):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	else:
		gallery = get_object_or_404(Gallery, slug=slug)
		return render(request, 'gallery/detail.html', {'gallery': gallery})


def galleryCreate(request):
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
		            'gallery': gallery,
		            'form': form,
		            'error_message': 'Image file must be PNG, JPG, or JPEG',
		        }
		        return render(request, 'gallery/gallery_form.html', context)
		    gallery.save()
		    messages.success(request, "Successfully Created!")
		    return HttpResponseRedirect(gallery.get_absolute_url())
		context = {
		    "form": form,
		}
		return render(request, 'gallery/gallery_form.html', context)

def galleryUpdate(request, slug):
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
					'gallery': gallery,
					'form': form,
					'error_message': 'Image file must be PNG, JPG, or JPEG',
					}
				return render(request, 'gallery/gallery_form.html', context)
		except MultiValueDictKeyError:
			gallery.gallery_image = gallery.gallery_image

		form.save()
		messages.success(request, "Successfully Editted!")
		return HttpResponseRedirect(gallery.get_absolute_url())
	return render(request, 'gallery/gallery_form.html', {'form': form})

def galleryDelete(request, slug):
	gallery = get_object_or_404(Gallery, slug=slug)
	gallery.delete()
	messages.error(request, "Successfully Deleted!")
	return HttpResponseRedirect('/my_gallery')


def imageCreate(request, slug):
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
		            'image': image,
		            'form': form,
		            'error_message': 'Image file must be PNG, JPG, or JPEG',
		        }
		        return render(request, 'gallery/image_form.html', context)
		    image.save()
		    messages.success(request, "Successfully Added!")
		    return HttpResponseRedirect(gallery.get_absolute_url())
		context = {
		    "form": form,
		}
		return render(request, 'gallery/image_form.html', context)


def imageDelete(request, slug, image_id):
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

class GallerySearchListView(ListView):
    model = Gallery
    template_name = 'gallery/featured.html'
    paginate_by = 10

    def get_queryset(self):
        all_gallery = Gallery.objects.all()
        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            vectors = SearchVector('gallery_title')
            all_gallery = all_gallery.annotate(search=vectors).filter(search=query)
        return all_gallery


def galleryFavorite(request, gallery_id):
	all_gallery = Gallery.objects.all()
	gallery = get_object_or_404(Gallery, pk=gallery_id)
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
		return HttpResponseRedirect("/featured")