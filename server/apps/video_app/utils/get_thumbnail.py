import os, subprocess
from django.conf import settings

THUMB = u'''ffmpeg -ss {0} -i "{1}" -vframes 1 -s 480x270 "{2}/{3}.jpg" -y'''
FNULL = open(os.devnull, 'w')
FOLDER = settings.MEDIA_ROOT + "/videos"


# TODO: Make this handle media with 4:3, 1.85:1 and 2.39:1 or aspect ratio as well
# currently assumes 16:9 for thumbnails
def get_thumbnail(path, duration):
    """ 
    generates video thumbnail 
    """
    thumnail_name = "_".join( path.split("/")[-1].split(".")[0].split(" ") )
    subprocess.Popen(
        THUMB.format( duration/3, path, FOLDER, thumnail_name ), 
        stdout=FNULL, 
        stderr=subprocess.STDOUT, 
        shell=True
    )
    return "/media/videos/{}.jpg".format(thumnail_name)