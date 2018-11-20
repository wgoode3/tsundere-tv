from django.http import JsonResponse
from .models import Anime, Video
from .utils import video_search, print_progressbar, transcode_media, stop_transcoding
from time import time
import os, binascii
from django.conf import settings

""" empty the database (for testing purposes) """
def reset(req):
    Anime.objects.all().delete()
    Video.objects.all().delete()
    return JsonResponse({'status': 200})

""" Trigger a search for media files on the server """
def media_search(req):
    """ 
    TODO: make thumbnail generation / jikan api call a separate process 
    AND/OR return a stream of information for a progress bar in the frontend
    using rxpy (https://github.com/ReactiveX/RxPY) and an rxjs observable 
    """
    
    print("locating videos...")
    
    time1 = time()
    videos = video_search()
    time2 = time()

    print("adding {} videos to the database...".format(len(videos)))
    i = 1
    for video in videos:
        Video.objects.add_video(video)
        print_progressbar(i, len(videos), prefix = 'Progress:', suffix = f"{i} of {len(videos)}", length = 50)
        i += 1
    
    time3 = time()
    
    print("completed in {} seconds...".format(time3-time1))
    
    msg1 = "found {} videos in {} seconds".format(len(videos), time2-time1)
    msg2 = "added to db in {} seconds".format(time3-time2)

    return JsonResponse({
        'status': 200, 
        "messages": [msg1, msg2]
    })

""" Return all video series, will be displayed to the dashboard page """
def get_all(req):
    return JsonResponse({
        'status': 200, 
        'all_anime': list(Anime.objects.values().all().order_by("title"))
    })

""" Return information about the anime with id: anime_id """
def get_anime(req, anime_id):
    return JsonResponse({
        'status': 200, 
        'anime': Anime.objects.values().get(id=anime_id),
        'videos': list(Video.objects.values().filter(anime_id=anime_id).order_by("episode_number"))
    })

""" Initiate the media transcoding in the backend && send the user to the video player """
def watch_anime(req, video_id):
    video = Video.objects.values().get(id=video_id)
    key = binascii.hexlify(os.urandom(16)).decode()
    pid = transcode_media(video['path'], key)
    return JsonResponse({
        'status': 200, 
        'host': settings.HOST,
        'id': video_id,
        'video': video,
        'key': key,
        'pid': pid
    })

def stop(req, pid):
    stop_transcoding(pid)
    return JsonResponse({'status': 200})