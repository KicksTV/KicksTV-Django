class Folder(object):
	folder_name = ''
	path_lower = ''
	sub_folder = []
	files = None

	def __init__(self, folder_name, path_lower):
		self.folder_name = folder_name
		self.path_lower = path_lower
		self.files = None

	def addFile(self,file):
		if self.files is None:
			self.files = []
		else:
			self.files.append(file)

	def getFiles(self):
		return self.files