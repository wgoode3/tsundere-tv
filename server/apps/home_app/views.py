# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from search import start
from play_media import play
import subprocess
from django.shortcuts import render, redirect
from django.conf import settings

def index(req):
	# kill any running instances of ffmpeg
	subprocess.Popen("killall ffmpeg", shell=True)
	return render(req, 'home_app/index.html')

def test(req):
	response = {
		'status': 200,
		'files': start()
	}
	return JsonResponse(response)

def vid(req):
	# should probably implement some sort of wait here!
	return JsonResponse({
		'status': 200, 
		'key': play(req.GET['path'])
	})

def watch(req):
	return render(req, 'home_app/watch.html', {
		'host': settings.ALLOWED_HOSTS[0], 
		'key': req.GET['key']
	})