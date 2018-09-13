from django.http import JsonResponse
from .models import Anime, Video

"""
Video view function stubs go here...
"""

""" Return all video series, will be displayed to the dashboard page """
def get_all(req):
    return JsonResponse({'status': 200})

""" Trigger a search for media files on the server """
def media_search(req):
    return JsonResponse({'status': 200})

""" Return information about the anime with id: anime_id """
def get_anime(req, anime_id):
    return JsonResponse({'status': 200, 'id': anime_id})

""" Initiate the media transcoding in the backend && send the user to the video player """
def watch_anime(req, video_id):
    return JsonResponse({'status': 200, 'id': video_id})
