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
	
	def merge_related(self):
		all_anime = Anime.objects.all()
		for anime in all_anime:
			dupes = Anime.objects.filter(mal_title=anime.mal_title)
			if len(dupes) > 1:
				# find the duplicate with the most videos
				has_most = max(dupes, key=lambda x: len(x.videos.all()))
				dupes.exclude(id=has_most.id)
				for dup in dupes:
					for video in dup.videos.all():
						# set foreign key to the entry with most videos
						video.anime = has_most
						video.save()
					# delete the duplicate
					Anime.objects.filter(id=dup.id).delete()
					all_anime.exclude(id=dup.id)

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

	def __repr__(self):
		return "<Anime object ({id}) {title}>".format(id=self.id, title=self.title)

	def __str__(self):
		return "<Anime object ({id}) {title}>".format(id=self.id, title=self.title)

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

		print("*"*100)
		print("at this point anime is", anime)
		print("*"*100)

		# first check for season number
		season = ""
		seasons = re.findall("((SECOND|THIRD|FOURTH)\ SEASON)|(SEASON\ (\d))|(S(\d))", anime, flags=re.IGNORECASE)
		if len(seasons) > 0:
			seasons = [s for s in seasons[0] if not s.isdigit() and len(s) > 0]
			if len(seasons) > 0:
				print("seasons arghhh!", seasons)
				season = max(seasons, key=len)

		# I'm also going to consider it safe to pull out season information
		if season != "":
			print("the season is!", season)
			anime = anime.replace(season, "")
			print("the anime is now!!!!", anime)

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

		# also check for specials
		is_special = False
		if episode == "":
			special = re.findall("(SP(\ )?(\d)+)|(SPECIAL(\ )?(\d)+)", anime, flags=re.IGNORECASE)
			print "what what what", special
			if len(special) > 0:
				special = [s for s in special[0] if not s.isdigit() and len(s) > 0]
				if len(special) == 1:
					episode = special[0]
					is_special = True

		""" This matches and splits off characters op and ed even in an anime name, not good """
		""" I'll try forcing a space at the start of the sequence """

		# also check for OP ED
		is_op_ed = False
		if episode == "":
			op_ed = re.findall("(\ NCOP(\d+)?|\ NCED(\d+)?|\ OP(\d+)?|\ ED(\d+)?)", anime, flags=re.IGNORECASE)
			print "why why why", op_ed
			if len(op_ed) > 0:
				op_ed = [o for o in op_ed[0] if not o.isdigit() and len(o) > 0]
				if len(op_ed) == 1:
					episode = op_ed[0]
					is_op_ed = True

		# determine the crc32 hash
		crc_hash = ""
		if len(brackets) > 0:
			if CRC32_HASH.match(brackets[-1]):
				crc_hash = brackets[-1]

		# I'm going to consider it safe to remove the episode number from the anime name
		# possible that episode number could also be in the name, that would be bad
		if episode != "":
			print("breaking things!", episode)
			anime = anime.split(episode)[0]

		anime = anime.strip()

		check = '''ffprobe -v error -show_entries stream '{}' '''
		b = subprocess.Popen(check.format(path), shell=True, stdout=subprocess.PIPE)
		out, err = b.communicate()
		streams = []
		stream = {}
		# split("\n") may sometimes give weird errors
		try:
			for line in out.splitlines():
				if line == "[STREAM]":
					stream = {}
				elif line == "[/STREAM]":
					streams.append(stream)
				else:
					if len(line.split("=")) == 2:
						stream[line.split("=")[0]] = line.split("=")[1]
		except UnicodeDecodeError as e:
			print("some weird unicode error here", e)
		subtitles = [s for s in streams if s["codec_type"] == 'subtitle']
		# print("*"*100)
		# print(subtitles)
		subs = ""
		for i in range(len(subtitles)):
			try:
				subs += "index=" + subtitles[i]["index"] + ","
				subs += "codec=" + subtitles[i]["codec_name"] + ","
				# print("the thing that is breaking", path)
				subs += "language=" + subtitles[i]["TAG:language"]
				if i < len(subtitles) - 1:
					subs += ";"
			except KeyError:
				break
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