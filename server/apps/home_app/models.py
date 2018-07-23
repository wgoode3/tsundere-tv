# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from django.db import models
from thumbs import thumbify
from requests import Session
import os, subprocess, re, difflib

CRC32_HASH = re.compile('^[0-9a-f]{8}$', flags=re.IGNORECASE)
SEARCH_URL = "https://api.jikan.moe/search/anime/{}"
session = Session()

class AnimeManager(models.Manager):
	def addAnime(self, anime):
		# check to see if the anime is already present
		# if it is return the id
		anime = anime.lower()
		print("about to look for", anime)
		match = Anime.objects.filter(title=anime)
		if len(match) > 0:
			return match[0].id
		else:
			newAnime = Anime()
			newAnime.title = anime

			# otherwise make an api call to jikan
			all_results = session.get(SEARCH_URL.format(anime)).json()["result"]
			titles = [result["title"].lower() for result in all_results]
			# use difflib to find the best match
			matches = difflib.get_close_matches(anime, titles, n=1, cutoff=0.5)
			entry = ""
			if len(matches) > 0:
				for result in all_results:
					if result["title"].lower() == matches[0]:
						entry = result
						break
			
				# fill in information accordingly
				newAnime.mal_title = entry["title"]
				newAnime.anime_type = entry["type"]
				newAnime.episodes = entry["episodes"]
				newAnime.mal_id = entry["mal_id"]
				newAnime.mal_url = entry["url"]
				newAnime.mal_img_url = entry["image_url"]
				newAnime.mal_score = entry["score"]
				newAnime.description = entry["description"]
			else:
				# if no match give it placeholder data
				newAnime.mal_score = 0.0
			newAnime.save()
			return newAnime.id

class Anime(models.Model):
	title = models.CharField(max_length=255)
	mal_title = models.CharField(max_length=255)
	anime_type = models.CharField(max_length=255)
	episodes = models.IntegerField(blank=True, null=True)
	mal_id = models.IntegerField(blank=True, null=True)
	mal_url = models.CharField(max_length=255)
	mal_img_url = models.CharField(max_length=255)
	mal_score = models.DecimalField(max_digits=4, decimal_places=2)
	description = models.CharField(max_length=255)

	objects = AnimeManager()

	def get_thumb(self):
		# return a link to a larger thumbnail image
		return self.mal_img_url.replace("/r/100x140/", "/")

class VideoManager(models.Manager):
	def addVideo(self, path):
		vid = Video()
		vid.path = path
		
		# extract the filename from the path
		vid.filename = path.split("/")[-1]

		# change underscores into spaces
		if vid.filename.find("_") > -1:
			vid.filename = vid.filename.replace("_", " ")

		# find all [] and () seperated sequences
		brackets = re.findall(r'\[(.*?)\]|\((.*?)\)', vid.filename)
		# combine the list of tuples of strings to a list of strings
		brackets = [b[0]+b[1] for b in brackets]

		# get everything not inside of [] or ()
		anime = ""
		paren = False
		for letter in vid.filename.split(".")[0]:
			if letter == "[" or letter == "(":
				paren = True
			elif letter == "]" or letter == ")":
				paren = False
			elif not paren:
				anime += letter

		anime = anime.strip()
		# also remove "-" that are inside of whitespace 
		anime = anime.replace(" - ", " ")

		# get episode number and handle v0, v2, etc releases
		episode = ""
		revision = re.findall(r'[0-9]+[\ ]?[v|V][0-9]+', anime)
		if len(revision) == 1:
			anime = anime.replace(revision[0], "")
			episode = revision[0]
		else:
			for a in reversed(anime.split(" ")):
				if a.isdigit():
					episode = a
					break
		# also handle OVA, ONA, and OAD
		is_ova = False
		if episode == "":
			ova = re.findall("ova|ona|oad", anime, flags=re.IGNORECASE)
			if len(ova) == 1:
				episode = ova[0]
				is_ova = True

		# look for season information
		# matches s2, S3, etc 
		# season = re.findall(r'[s|S]+[0-9]+', anime)

		# parts = re.findall(r"[\w']+", vid.filename)
		# if len(parts) > 2:
		# 	vid.sub_group = parts[0]
		# 	for part in parts:
		# 		if part.isdigit():
		# 			vid.episode_number = int(part)

		# determine the crc32 hash
		crc_hash = ""
		if len(brackets) > 0:
			if CRC32_HASH.match(brackets[-1]):
				crc_hash = brackets[-1]

		# I'm going to consider it safe to remove the episode number from the anime name
		# possible that episode number could also be in the name, that would be bad
		if episode != "":
			anime = anime.split(episode)[0]

		anime = anime.strip()

		check = '''ffprobe -v error -show_entries stream '{}' '''
		b = subprocess.Popen(check.format(path), shell=True, stdout=subprocess.PIPE)
		out, err = b.communicate()
		streams = []
		stream = {}
		for line in out.split("\n"):
			if line == "[STREAM]":
				stream = {}
			elif line == "[/STREAM]":
				streams.append(stream)
			else:
				if len(line.split("=")) == 2:
					stream[line.split("=")[0]] = line.split("=")[1]
		subtitles = [s for s in streams if s["codec_type"] == 'subtitle']
		# print("*"*100)
		# print(subtitles)
		subs = ""
		for i in range(len(subtitles)):
			subs += "index=" + subtitles[i]["index"] + ","
			subs += "codec=" + subtitles[i]["codec_name"] + ","
			# print("the thing that is breaking", path)
			subs += "language=" + subtitles[i]["TAG:language"]
			if i < len(subtitles) - 1:
				subs += ";"
		vid.subtitles = subs
		response = thumbify(path)
		vid.duration = response["duration"]
		vid.thumb = response["thumb"] + ".jpg"
		vid.crc_hash = crc_hash
		vid.episode_number = episode
		vid.filesize = os.stat(path).st_size # gives me filesize in bytes
		print("the anime is", anime)
		vid.anime_id = Anime.objects.addAnime(anime)
		print("saving video", vid.__dict__)
		vid.save()

class Video(models.Model):
	path = models.CharField(max_length=255)
	filename = models.CharField(max_length=255)
	sub_group = models.CharField(max_length=255)
	episode_number = models.CharField(max_length=255)
	subtitles = models.CharField(max_length=255)
	duration = models.CharField(max_length=255)
	thumb = models.CharField(max_length=255)
	crc32_hash = models.CharField(max_length=8)
	filesize = models.IntegerField()
	anime = models.ForeignKey(Anime, related_name="videos")

	objects = VideoManager()

	def get_duration(self):
		# return a human readable value for duration
		d = float(self.duration)
		h = int(d/3600)
		d %= 3600
		m = str(int(d/60))
		if len(m) == 1: m = "0"+m
		d %= 60
		s = str(int(d))
		if len(s) == 1: s = "0"+s
		return "{h}:{m}:{s}".format(h=h, m=m, s=s)

	def get_filesize(self):
		# return a human readable value for filesize
		if self.filesize < 10**3:
			return "{}B".format(self.filesize)
		elif self.filesize < 10**6:
			return "{:.2f}KB".format(self.filesize / 1024)
		elif self.filesize < 10**9:
			return "{:.2f}MB".format(self.filesize / 1024**2)
		else:
			return "{:.2f}GB".format(self.filesize / 1024**3)