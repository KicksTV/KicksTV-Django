class File(object):
	file_name = ''
	path_lower = ''
	client_modified = ''
	server_modified = ''
	size = ''

	def __init__(self, file_name, path_lower, client_modified, server_modified, size):
		self.file_name = file_name
		self.path_lower = path_lower
		self.client_modified = client_modified
		self.server_modified = server_modified
		self.size = size
