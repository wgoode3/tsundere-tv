# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from search import start

from django.shortcuts import render, redirect

def index(req):
	return render(req, 'home_app/index.html')

def test(req):
	response = {
		'status': 200,
		'files': start()
	}
	return JsonResponse(response)

def vid(req):
	print "the path is", req.GET['path']
	return JsonResponse({'status': 200})