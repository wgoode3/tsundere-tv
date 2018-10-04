from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import User
from django.views import View

class Users(View):

    """ Get all """
    def get(self, req):
        return JsonResponse({'status': 200, 'users': list(User.objects.values().all())})

    """ Register method """
    def post(self, req):
        results = User.objects.register(json.loads(req.body.decode()))
        if isinstance(results, User):
            req.session['user_id'] = results.id
            return JsonResponse({'status': 200, 'user_id': results.id})
        else:
            return JsonResponse({'status': 200, 'errors': results})

class UsersSession(View):

    """ Get session """
    def get(self, req):
        if 'user_id' in req.session:
            return JsonResponse({'status': 200, 'user_id': req.session['user_id']})
        else:
            return JsonResponse({'status': 200})

    """ Login method """
    def post(self, req):
        results = User.objects.login(json.loads(req.body.decode()))
        if isinstance(results, User):
            req.session['user_id'] = results.id
            return JsonResponse({'status': 200, 'user_id': results.id})
        else:
            return JsonResponse({'status': 200, 'errors': results})

    """ Logout method """
    def delete(self, req):
        req.session.clear()
        return JsonResponse({'status': 200})

class UsersDetail(View):

    """ Get one user """
    def get(self, req, user_id):
        return JsonResponse({'status': 200, 'user': User.objects.values().get(id=user_id)})

    """ Update the user """
    def put(self, req, user_id):
        User.objects.update(json.loads(req.body.decode()), user_id)
        return JsonResponse({'status': 200})

    """ Delete the user """
    def delete(self, req, user_id):
        return JsonResponse({'status': 200})