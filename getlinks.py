#!/usr/bin/env python

import sys
import string
import os.path
import requests
from urlparse import urlparse

LINKS = []

# ------------------------------------------------------------ #
def check_folder( url ):
	result = urlparse(url)
	folder = result.path[1:-1]

	if not os.path.exists("links"):
		os.mkdir("links")
		print("folder links created")

	return folder

# ------------------------------------------------------------ #
def load_links( path, index ):
	url = "{}{}".format(path, index)
	headers = { "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30" }
	print("get:", url)
	r = requests.get(url, headers=headers)
	print("done!")

	data = r.text
	print("read content...")
	indexStart = string.find(data, "article__content")
	if indexStart > 0:
		indexEnd = string.find(data, "section", indexStart)
		section = data[indexStart-16:indexEnd]

		links = []
		index = 0
		maxc = 1000
		while index >= 0 and maxc > 0:
			maxc -= 1
			# print("start with:", index)
			a = string.find(section, "<a href", index)
			if a > 0:
				b = string.find(section, "><", a)
				s = section[a+9:b-1]
				LINKS.append(s)
				index = b
			else:
				index = -1
	print("done!")

		

# ------------------------------------------------------------ #
def get_data( url, count ):
	folder = check_folder(url)

	# load_links(url, 1)
	for i in range(1, count+1):
		load_links(url, i)

	with open('links/{}.txt'.format(folder), 'w') as file:
		    file.write('\n'.join(LINKS))

# ------------------------------------------------------------ #
def main( argv ):
	total = len( argv )
	url = None
	count = 0
	if total > 1:
		url = argv[1]
	if total > 2:
		count = int(argv[2])
	if url:
		get_data(url, count)

# ------------------------------------------------------------ #
#  Main  #
# ------------------------------------------------------------ #
if __name__ == "__main__":
	main( sys.argv )
