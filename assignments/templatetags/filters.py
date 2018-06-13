from django import template
from assignments.folder import Folder

register = template.Library()
	
def runFiles(value, args):
	return args.getFiles()

register.filter('runFiles', runFiles)