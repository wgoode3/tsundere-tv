from django.db import models
from ..user_app.models import User
from .utils import parse_filename, get_filesize, get_duration, get_thumbnail, get_subtitles, search_jikan, download_thumbnail
import os, subprocess, re, difflib


class AnimeManager(models.Manager):
    def add_anime(self, anime_name):
        try:
            anime = Anime.objects.get(title__iexact=anime_name)
        except Anime.DoesNotExist:
            if anime_name == "unknown":
                anime = Anime.objects.create(
                    title = "unknown",
                    thumbnail = "/media/anime/unknown.jpg"
                )
            else:
                mal_entry = search_jikan(anime_name)
                thumb = download_thumbnail(anime_name, mal_entry['image_url'])
                anime = Anime.objects.create(
                    title = anime_name,
                    mal_id = mal_entry['mal_id'],
                    mal_title = mal_entry['title'],
                    anime_type = mal_entry['type'],
                    episodes = mal_entry['episodes'],
                    mal_url = mal_entry['url'],
                    mal_score = mal_entry['score'],
                    description = mal_entry['description'],
                    thumbnail = thumb
                )
        return anime

    def merge_related(self):
        return True


class Anime(models.Model):
    title = models.CharField(max_length=255)
    mal_id = models.IntegerField(blank=True, null=True)
    mal_title = models.CharField(max_length=255)
    anime_type = models.CharField(max_length=255)
    episodes = models.IntegerField(blank=True, null=True)
    mal_url = models.CharField(max_length=255)
    mal_score = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.CharField(max_length=255)
    thumbnail = models.CharField(max_length=255, default="unknown.jpg")

    objects = AnimeManager()

    def __repr__(self):
        return "<Anime object: ({id}) ({title})>".format(id=self.id, title=self.title)

    def __str__(self):
        return "<Anime object: ({id}) ({title})>".format(id=self.id, title=self.title)


class VideoManager(models.Manager):
    def add_video(self, path):
        try:
            video = Video.objects.get(path=path)
        except Video.DoesNotExist:
            vid = Video()
            vid.path = path
            vid.filename = path.split("/")[-1]
            
            """ 
            put the parsed attributes into the object
            it may be easier to just pass vid into the parse_filename function...
            """
            file = parse_filename(vid.filename)
            for attr in file:
                setattr(vid, attr, file[attr])

            vid.filesize = get_filesize(path)
            vid.duration = get_duration(path)
            vid.subtitles = get_subtitles(path)
            vid.thumbnail = get_thumbnail(path, vid.duration)

            if 'anime_name' not in vid.__dict__:
                vid.anime_name = "unknown"

            vid.anime = Anime.objects.add_anime(vid.anime_name)
            vid.save()


class Video(models.Model):
    path = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    fansub_group = models.CharField(max_length=255)
    episode_number = models.CharField(max_length=255)
    subtitles = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    thumbnail = models.CharField(max_length=255, default="unknown.jpg")
    crc32_hash = models.CharField(max_length=8)
    filesize = models.IntegerField(blank=True, null=True)
    anime = models.ForeignKey(Anime, related_name="videos", on_delete=models.CASCADE)

    objects = VideoManager()

    def __repr__(self):
        return "<Video object: ({id}) ({filename})>".format(id=self.id, filename=self.filename)

    def __str__(self):
        return "<Video object: ({id}) ({filename})>".format(id=self.id, filename=self.filename)


""" keep track of what media a user has watched and where they stopped """
"""
class ViewHistory(models.Model):
    user = models.ForeignKey(User, related_name="history", on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name="viewed_by", on_delete=models.CASCADE)
    # True is completed
    completed = models.BooleanField()
    # Number of seconds watched (rounded down)... so user can resume playback
    position = models.IntegerField(blank=True, null=True) 

"""