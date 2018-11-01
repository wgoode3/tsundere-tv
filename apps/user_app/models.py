from django.conf import settings
from django.db import models
from PIL import Image
from io import BytesIO
import os, re, bcrypt, base64

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')


""" resize an image, preserving aspect ratio and keeping it centerred """
def resizer(img, w, h):
    offset_x, offset_y = 0, 0
    if img.width / img.height > w / h:
        new_width = w*img.height//h
        offset_x = (img.width - new_width)//2
    else:
        new_height = h*img.width//w
        offset_y = (img.height - new_height)//2
    img = img.crop( ( offset_x, offset_y, img.width - offset_x, img.height - offset_y) )
    img = img.resize( (w, h), Image.ANTIALIAS)
    return img


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

    def update(self, data, user_id):
        user = User.objects.get(id=user_id)
        if 'filename' in data and 'image' in data:
            if data['filename'].split('.')[-1].lower() in settings.ALLOWED_EXTENSIONS:
                img_path = os.path.join(settings.MEDIA_ROOT, 'avatars', data['filename'])
                with open(img_path, 'wb') as img:
                    img.write(base64.b64decode(data['image'].split(',')[-1]))
                    user.avatar = data['filename']
                i = Image.open(img_path)
                i = resizer(i, 128, 128)
                i.save(img_path)
                i.close()
        if data['username'] != user.username and len(data['username']) > 2:
            try:
                User.objects.get(username=data['username'])
            except User.DoesNotExist:
                if bcrypt.checkpw(data['password'].encode(), user.password.encode()):
                    user.username = data['username']
        user.save()


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