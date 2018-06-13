import socket


if socket.gethostname()=="kickstv-VirtualBox":
    from .local import *
else:
	from .production import *

