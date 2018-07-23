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
	# VIDEOS[0] = []
	# results = search(os.path.expanduser("~"))
	search(os.path.expanduser("~"))
	# print "results are:", results
	# gen_keys(results)
	# return results
# 
def gen_keys(results):
	print "results here:", results
	for r in results:
		
		print "*"*100
		print "path is", r
		
		fn = r.split("/")[-1]
		fn = " ".join(fn.split("_"))

		print "file name is", fn
		
		parts = re.findall(r"[\w']+", fn)
		print parts
		if len(parts) > 2:
			print "sub group is", parts[0]

			# find episode number
			for part in parts:
				if part.isdigit():
					print "episode number = ", part

		check = '''ffmpeg -i '{}' -c copy -map 0:s -f null - -v 0 -hide_banner && echo $? || echo $?'''
		a = subprocess.Popen(check.format(r), shell=True, stdout=subprocess.PIPE)
		out, err = a.communicate()
		# print "out is", out.strip(), "err is", err
		if out.strip() == "0":
			print "there are subtitles"
		else:
			print "there are not subtitles"

		# parse stream information from ffprobe
		check2 = '''ffprobe -v error -show_entries stream '{}' '''
		b = subprocess.Popen(check2.format(r), shell=True, stdout=subprocess.PIPE)
		out, err = b.communicate()
		# print "out is", out.strip(), "err is", err
		streams = []
		stream = {}
		for line in out.split("\n"):
			if line == "[STREAM]":
				stream = {}
			elif line == "[/STREAM]":
				streams.append(stream)
			else:
				# print line.split("=")
				if len(line.split("=")) == 2:
					stream[line.split("=")[0]] = line.split("=")[1]
		streams = [s for s in streams if s["codec_type"] == 'subtitle']
		print streams

		# subtitles information from ffprobe
		print "there are", len(streams), "subtitle tracks"
		for i in range(len(streams)):
			print "\tindex #" + streams[i]["index"]
			# print "\tsubtitles #{}".format(i+1)
			print "\tcodec =", streams[i]["codec_name"]
			print "\tlanguage =", streams[i]["TAG:language"]


