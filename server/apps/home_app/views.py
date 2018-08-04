# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from search import vid_search
from play_media import play
import subprocess
from .models import Anime, Video

def index(req):
	# kill any running instances of ffmpeg
	subprocess.Popen("killall ffmpeg", shell=True)
	data = {
		"anime": Anime.objects.all().order_by('mal_title')
	}
	return render(req, 'home_app/index.html', data)

def test(req):
	# really should consider not going back to square one each time
	Video.objects.all().delete()
	# find all the anime
	vid_search()
	# sometimes an anime gets considered 2 seperate anime
	# this merges them back ...
	# seems broken
	# Anime.objects.merge_related()
	return redirect("/")

def anime(req, anime_id):
	anime = Anime.objects.get(id=anime_id)
	videos = anime.videos.all().order_by('episode_number')

	return render(req, 'home_app/anime.html', {"anime": anime, 'videos': videos})

def vid(req):
	# should probably implement some sort of wait here!
	return JsonResponse({
		'status': 200,
		'host': settings.ALLOWED_HOSTS[0], 
		'key': play(req.GET['path'])
	})

def watch(req):
	return render(req, 'home_app/watch.html', {
		'host': settings.ALLOWED_HOSTS[0], 
		'key': req.GET['key']
	})