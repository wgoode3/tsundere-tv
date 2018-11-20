from PIL import Image
from io import BytesIO
from requests import Session
from django.conf import settings

session = Session()

# These values work well probably no need to make them configurable
DEFAULT_WIDTH = 200
DEFAULT_HEIGHT = 300


def resizer(img, w, h):
    """ 
    resizes an image, preserving aspect ratio and keeping it centerred 
    """
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


def download_thumbnail(anime, url):
    """ 
    saves a thumbnail image for the anime from MAL 
    """
    thumbnail_name = "/anime/" + "_".join(anime.split(" ")) + ".jpg"
    r = session.get(url, stream=True)
    img = resizer(Image.open(BytesIO(r.content)), DEFAULT_WIDTH, DEFAULT_HEIGHT)
    img.save(settings.MEDIA_ROOT + thumbnail_name)
    img.close()
    return "/media" + thumbnail_name