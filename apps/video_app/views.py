from django.http import JsonResponse
from .models import Anime, Video
from .utils import video_search, printProgressBar
from time import time


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

    print(f"adding {len(videos)} videos to the database...")
    i = 1
    for video in videos:
        Video.objects.add_video(video)
        printProgressBar(i, len(videos), prefix = 'Progress:', suffix = f"{i} of {len(videos)}", length = 50)
        i += 1
    
    time3 = time()
    
    print(f"completed in {time3-time1} seconds...")
    
    msg1 = f"found {len(videos)} videos in {time2-time1} seconds"
    msg2 = f"added to db in {time3-time2} seconds"

    return JsonResponse({
        'status': 200, 
        "messages": [msg1, msg2]
    })

""" Return all video series, will be displayed to the dashboard page """
def get_all(req):
    return JsonResponse({
        'status': 200, 
        'all_anime': list(Anime.objects.values().all())
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
    return JsonResponse({'status': 200, 'id': video_id})
