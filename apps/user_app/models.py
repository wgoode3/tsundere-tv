from django.conf import settings
from django.db import models
from PIL import Image
from io import BytesIO
import re, bcrypt, base64, os

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def register(self, data):

        errors = {}

        """ username validations """
        if len(data['username']) < 1:
            errors['username'] = 'Username is required!'
        elif len(data['username']) < 3:
            errors['username'] = 'Username must be 3 characters or longer!'
        else:
            try:
                User.objects.get(username=data['username'])
                errors['username'] = 'Username is already in use!'
            except User.DoesNotExist: 
                pass

        """ password validations """
        if len(data['password']) < 1:
            errors['password'] = 'Password is required!'
        elif len(data['password']) < 8:
            errors['password'] = 'Password must be 8 characters or longer!'

        """ confirm password validations """
        if len(data['confirm']) < 1:
            errors['confirm'] = 'Confirm Password is required!'
        elif data['confirm'] != data['password']:
            errors['confirm'] = 'Confirm Password must match Password!'

        if len(errors) > 0:
            errors['valid'] = False
            return errors
        else:
            return User.objects.create(
                username = data['username'],
                password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
            )
    
    def login(self, data):
        user = User.objects.get(id=data['id'])
        if bcrypt.checkpw(data['password'].encode(), user.password.encode()):
            return user
        else:
            return {'password': 'Incorrect password'}
        return True

    def update(self, data, user_id):
        user = User.objects.get(id=user_id)
        if 'filename' in data and 'image' in data:
            if data['filename'].split('.')[-1].lower() in settings.ALLOWED_EXTENSIONS:
                with open(os.path.join(settings.MEDIA_ROOT, 'avatars', data['filename']), 'wb') as img:
                    img.write(base64.b64decode(data['image'].split(',')[-1]))
                    user.avatar = data['filename']
        user.username = data['username']
        user.save()
        return True


class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255, default="unknown.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return "<User object: ({id}) ({username})>".format(id=self.id, username=self.username)

    def __str__(self):
        return "<User object: ({id}) ({username})>".format(id=self.id, username=self.username)