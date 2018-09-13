from django.db import models

# need to pip install requests
# from requests import Session

import os, subprocess, re, difflib

CRC32_HASH = re.compile('^[0-9a-f]{8}$', flags=re.IGNORECASE)
SEARCH_URL = "https://api.jikan.moe/search/anime/{}"
# session = Session()

class AnimeManager(models.Manager):
    def add_anime(self, anime):
        return True
    
    def merge_related(self):
        return True

class Anime(models.Model):
    # go off the MAL Title if available
    title = models.CharField(max_length=255)
    # episode / movie / ova / oad
    anime_type = models.CharField(max_length=255)
    # the number of episodes
    episodes = models.IntegerField(blank=True, null=True)
    # the id from MAL (my anime list)
    mal_id = models.IntegerField(blank=True, null=True)
    # the URL to the MAL page
    """
    check documentation if there is a field for urls 
    """
    mal_url = models.CharField(max_length=255)
    # the URL to the anime image
    mal_img_url = models.CharField(max_length=255)
    # meaningless score from MAL
    mal_score = models.DecimalField(max_digits=4, decimal_places=2)
    # the description from MAL
    description = models.CharField(max_length=255)

    objects = AnimeManager()

    """
    should just save the image instead...
    """
    def get_thumb(self):
        # return a link to the larger thumbnail image
        return True

    def __repr__(self):
        return "<Anime object: ({id}) ({title})>".format(id=self.id, title=self.title)

    def __str__(self):
        return "<Anime object: ({id}) ({title})>".format(id=self.id, title=self.title)

class VideoManager(models.Manager):
    def add_video(self, path):
        return True

class Video(models.Model):
    """
    check documentation for a field for file paths
    """
    path = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    fansub_group = models.CharField(max_length=255)
    episode_number = models.CharField(max_length=255)
    subtitles = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    thumbnail = models.CharField(max_length=255)
    crc32_hash = models.CharField(max_length=8)
    filesize = models.IntegerField()
    anime = models.ForeignKey(Anime, related_name="videos", on_delete=models.CASCADE)

    objects = VideoManager()

    """
    returns a human readable value for duration
    """
    def get_duration(self):
        d = float(self.duration)
        h = int(d/3600)
        d %= 3600
        m = str(int(d/60))
        if len(m) == 1: m = "0"+m
        d %= 60
        s = str(int(d))
        if len(s) == 1: s = "0"+s
        return "{h}:{m}:{s}".format(h=h, m=m, s=s)

    """
    returns a human readable value for filesize
    """
    def get_filesize(self):
        if self.filesize < 10**3:
            return "{}B".format(self.filesize)
        elif self.filesize < 10**6:
            return "{:.2f}KB".format(self.filesize / 1024)
        elif self.filesize < 10**9:
            return "{:.2f}MB".format(self.filesize / 1024**2)
        else:
            return "{:.2f}GB".format(self.filesize / 1024**3)