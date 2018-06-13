import dropbox

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .dropboxConfig import dropboxToken


from .models import Folder, SubFolder, File
from .folder import Folder
from .file import File
# Create your views here.

FILE_TYPES = ['docx']

token = dropboxToken


def moduleView(request):
	dbx = dropbox.Dropbox(token)
	allFolders = []
	allFiles = []
	
	for entry in dbx.files_list_folder('', True).entries:
		if "." not in entry.name:
			newFolder = Folder(entry.name, entry.path_lower)
			allFolders.append(newFolder)

		if "." in entry.name:
			print(newFolder.folder_name)
			newFile = File(entry.name, entry.path_lower, entry.client_modified, entry.server_modified, entry.size)		
			newFolder.addFile(newFile)
		
	for folder in allFolders:
		print(folder.folder_name)
		if folder.getFiles() is not None:
			for file in folder.getFiles():
				print(file.file_name)					

	return render(request, "assignments/index.html", {
		'allFolders': allFolders,
		})

def courseWorkView(request, module_id):
	module = get_object_or_404(Module, pk=module_id)
	return render(request, "assignments/courseWork.html", {'module': module})

def createModule(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	else:
		form = ModuleForm(request.POST or None, request.FILES or None)
		if form.is_valid():
		    module = form.save(commit=False)
		    module.save()
		    return HttpResponseRedirect(reverse('courseWork', args=(
				module.id,)))
		context = {
		    "form": form,
		}
		return render(request, 'assignments/module_form.html', context)

def deleteModule(request, module_id):
	module = get_object_or_404(Module, pk=module_id)
	module.delete()
	return HttpResponseRedirect(reverse('modules'))

def createCourseWork(request, module_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login')
	else:
		form = CourseWorkForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			module = get_object_or_404(Module, pk=module_id)
			courseWorkNew = form.save(commit=False)
			courseWorkNew.module = module
			courseWorkNew.courseWork_file = request.FILES['courseWork_file']
			courseWorkNew.courseWork_title = courseWorkNew.courseWork_file.name
			file_type = courseWorkNew.courseWork_file.url.split('.')[-1]
			file_type = file_type.lower()
			if file_type not in FILE_TYPES:
				context = {
				    'courseWork': courseWorkNew,
				    'form': form,
				    'error_message': 'File Must Be .docx',
				}
				return render(request, 'assignments/module_form.html', context)
			courseWorkNew.save()
			return HttpResponseRedirect(reverse('courseWork', args=(
					module.id,)))
		context = {
		    "form": form,
		}
		return render(request, 'assignments/module_form.html', context)

def folderView(request, folder):
	return;