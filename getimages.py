#!/usr/bin/env python

import sys
import string
import os.path
import requests
from urlparse import urlparse

LINKS = []

# ------------------------------------------------------------ #
def check_folder( folder ):
	if not os.path.exists("images"):
		os.mkdir("images")
		print("folder images created")

	path = os.path.join("images", folder)
	if not os.path.exists(path):
		os.mkdir(path)
		print("folder {} created".format(path))

# ------------------------------------------------------------ #
def load_image( folder, path ):
	headers = { "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30" }
	print("get:", path)
	image = requests.get(path, headers=headers).content
	print("done!")
	
	print("saving image...")
	indexSlash = string.rfind(path, "/")
	filename = path[indexSlash+1:len(path)]
	with open('images/{}/{}'.format(folder, filename), 'wb') as handler:
	    handler.write(image)
	print("done!")

		

# ------------------------------------------------------------ #
def get_data( filename, skip ):
	check_folder(filename)

	index = 0
	with open('links/{}.txt'.format(filename)) as f:
	    lines = f.readlines()
	    for line in lines:
	    	index += 1
	    	if index >= skip:
		    	load_image(filename, line.rstrip('\n'))

# ------------------------------------------------------------ #
def main( argv ):
	total = len( argv )
	skip = 0
	filename = None
	if total > 1:
		filename = argv[1]
	if total > 2:
		skip = int(argv[2])
	if filename:
		get_data(filename, skip)

# ------------------------------------------------------------ #
#  Main  #
# ------------------------------------------------------------ #
if __name__ == "__main__":
	main( sys.argv )
