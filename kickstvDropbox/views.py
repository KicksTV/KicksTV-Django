import dropbox

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.encoding import smart_str
from KicksTV.settings.local import BASE_DIR

from .dropboxConfig import dropboxToken


# from .models import Folder, SubFolder, File
from .custom_class import File
# Create your views here.

FILE_TYPES = ['docx']

token = dropboxToken
dbx = dropbox.Dropbox(token)


def getFolderPath(path):
	path = path.split("/")
	newPath = ""
	for p in path:
		if "." not in p:
			newPath += p+"/"

	return newPath

def createEntries():
	
	allGroups = []
	allfiles = []
	path = None
	for entry in dbx.files_list_folder('', True).entries:
		doesExist = False
		if "." in entry.path_lower:
			if path is not None:
				for g in path:
					if getFolderPath(entry.path_lower) == g:
						doesExist = True
			else:
				path = []
				path.append(getFolderPath(entry.path_lower))
				doesExist = True
			
			if doesExist == False:
				path.append(getFolderPath(entry.path_lower))
	
	for p in path:
		group = []
		group.append(p)
		allGroups.append(group)

	for entry in dbx.files_list_folder('', True).entries:
		if "." in entry.path_lower:
			newFile = File(entry.name, entry.path_lower, entry.client_modified, entry.server_modified, entry.size)
			for group in allGroups:
				if getFolderPath(newFile.path_lower) == group[0]:
					group.append(newFile)
	return allGroups

def moduleView(request):
	
	paths = []
	allGroups = createEntries()
	# for group in allGroups:
	# 	print(group[0])
	# 	for file in group:
	# 		if type(file) == File:
	# 			print(file.file_name)
	for group in allGroups:
		paths.append(group[0])
		

	for group in allGroups:
		num = 0
		del group[0]

		for file in group:
			if num == 0:
				file.path_lower = getFolderPath(file.path_lower)
				num += 1

	return render(request, "dropbox/index.html", {
		'allGroups': allGroups,
		'paths': paths,
		})

allGroups = createEntries()
def fileDownloadView(request, file):
	if "." not in file:
		for group in allGroups:
			num = 0
			for getFile in group:
				if num == 1:
					file = getFile.path_lower
				num += 1


	dbx.files_download_to_file(BASE_DIR + "/file", file)
	with open(BASE_DIR+"/file", "rb") as f:
		response = HttpResponse(f.read())
		response['content_type']= 'application/force-download'
		response['Content-Disposition'] = 'attachment; filename=file'
		return response
