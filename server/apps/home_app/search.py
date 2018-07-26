# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Video
import os, re, subprocess
# from thumbs import thumbify

VIDEOS = [[]]
# extensions = ("mkv", "avi", "ogm", "mp4", "webm")
extensions = ("mkv",)

def search(loc):
	ls = os.listdir(loc)
	for thing in ls:
		if os.path.isdir(os.path.join(loc, thing)):
			if not thing.startswith("."):
				search(os.path.join(loc, thing))
		elif os.path.isfile(os.path.join(loc, thing)):
			if thing.split(".")[-1] in extensions:
				print "video found:", thing
				Video.objects.addVideo(os.path.join(loc, thing))
				# VIDEOS[0].append(os.path.join(loc, thing))
	# return VIDEOS[0]

# returns a list paths to all videos matching the allowed extensions
def vid_search():
	print "starting search"
	search(os.path.expanduser("/media/sf_shared"))
	# search(os.path.expanduser("~"))
