# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from search import start
from play_media import play
import subprocess

from django.shortcuts import render, redirect

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
	return JsonResponse({'status': 200, 'key': play(req.GET['path'])})

def watch(req):
	return render(req, 'home_app/watch.html', {'key': req.GET['key']})