from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import User
import json


class Users(View):
    def get(self, req):
        """ 
        gets all users
        """
        return JsonResponse({'status': 200, 'users': list(User.objects.values().all())})

    def post(self, req):
        """ 
        registers a new user
        """
        results = User.objects.register(json.loads(req.body.decode()))
        if isinstance(results, User):
            req.session['user_id'] = results.id
            return JsonResponse({'status': 200, 'user_id': results.id})
        else:
            return JsonResponse({'status': 200, 'errors': results})


class UsersSession(View):
    def get(self, req):
        """ 
        returns the session variable 
        """
        if 'user_id' in req.session:
            return JsonResponse({'status': 200, 'user_id': req.session['user_id']})
        else:
            return JsonResponse({'status': 200})

    def post(self, req):
        """ 
        logs a user in 
        """
        results = User.objects.login(json.loads(req.body.decode()))
        if isinstance(results, User):
            req.session['user_id'] = results.id
            return JsonResponse({'status': 200, 'user_id': results.id})
        else:
            return JsonResponse({'status': 200, 'errors': results})

    def delete(self, req):
        """ 
        logs a user out
        """
        req.session.clear()
        return JsonResponse({'status': 200})


class UsersDetail(View):
    def get(self, req, user_id):
        """
        returns the user with id = user_id
        """
        return JsonResponse({'status': 200, 'user': User.objects.values().get(id=user_id)})

    def put(self, req, user_id):
        """ 
        updates the user with id = user_id
        """
        User.objects.update(json.loads(req.body.decode()), user_id)
        return JsonResponse({'status': 200})

    def delete(self, req, user_id):
        """ 
        deletes the user with id = user_id 
        """
        return JsonResponse({'status': 200})