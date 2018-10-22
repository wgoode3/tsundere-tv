import os, subprocess, shutil, re, difflib
from requests import Session

session = Session()

VIDEOS = [[]]
ALLOWED_EXTENSIONS = ( "mkv" )
CRC32_HASH = re.compile('^[0-9A-F]{8}$')
DURATION = u'''ffprobe -i "{}" -show_entries format=duration -v quiet -of csv="p=0"'''
THUMB = u'''ffmpeg -ss {0} -i "{1}" -vframes 1 -s 480x270 "{2}/{3}.jpg" -y'''
FNULL = open(os.devnull, 'w')
FOLDER = os.getcwd() + "/media/videos"
CHECK = u'''ffprobe -v error -show_entries stream '{}' '''
SEARCH_URL = "https://api.jikan.moe/search/anime/?q={}"


""" finding media files to manage """
def search( loc ):
    ls = os.listdir( loc )
    for thing in ls:
        if not thing.startswith( "." ):
            if os.path.isdir( os.path.join( loc, thing ) ):
                search( os.path.join( loc, thing ) )
            elif os.path.isfile( os.path.join( loc, thing ) ):
                if thing.split(".")[-1] in ALLOWED_EXTENSIONS:
                    VIDEOS[0].append( os.path.join( loc, thing ) )

def video_search():
    VIDEOS[0] = [] 
    search( os.path.expanduser( "~" ) )
    return VIDEOS[0]


""" 
printing a progress bar 
from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
"""
def printProgressBar ( iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█' ):
    percent = ( "{0:." + str( decimals ) + "f}" ).format( 100 * ( iteration / float( total ) ) )
    filledLength = int( length * iteration // total )
    bar = fill * filledLength + '-' * ( length - filledLength )
    print( '\r%s |%s| %s%% %s' % ( prefix, bar, percent, suffix ), end = '\r' )

    if iteration == total: 
        print()


""" splitting up the filename """
def unbracket(path):
    path = path.split( "/" )[-1]

    brackets = []
    parenthesis = []
    rest_of_name = ''
    paren = False
    bracket = False

    for letter in path:
        if letter == '(':
            paren = True
            parenthesis.append( '' )
        elif letter == ')':
            paren = False
        elif letter == '[':
            bracket = True
            brackets.append( '' )
        elif letter == ']':
            bracket = False
        elif paren:
            parenthesis[-1] += letter
        elif bracket:
            brackets[-1] += letter
        elif letter == "_":
            rest_of_name += " "
        else:
            rest_of_name += letter

    return brackets, parenthesis, rest_of_name.split( "." )[0]


""" parse filename to determin information about the file """
def parse_filename( file ):

    d = {}

    """ determine the fansub group """
    if file.startswith( "[" ) and file.find( "]" ) > 0:
        d['fansub_group'] = file[1:file.find("]")]

    """ remove underscores """
    file = file.replace( "_", " " )

    """ filter out text inside of brackets and parenthesis """
    b, p, r = unbracket( file )

    """ find the CRC32 hash value """
    # result tends to be at the end of the brackets, so reversed should be faster
    for val in reversed(p + b):
        if CRC32_HASH.match(val):
            d['crc32_hash'] = val
            break

    """ check for season """
    season = re.findall("((1st|2nd|3rd|4th|5th|first|second|third|forth|fifth)\ season)|(s\d)|(season\ \d)", file, flags=re.IGNORECASE)
    if len(season) > 0:
        season = max(season[0], key=len)
        r = r.replace(season, '')
        d['season'] = season

    episode = ''

    """ check if it is an op or an ed """
    op_ed = re.findall("(\ op|\ ed|\ ncop|\ nced|\ OP|\ ED|\ NCOP|\ NCED)[\ ]?(\d+)?", r)
    op_ed = [''.join(o for o in op).strip() for op in op_ed]
    if len(op_ed) > 0:
        episode = max(op_ed, key=len)

    """ check if it is an ova or oad """
    if len(episode) < 1:
        ova = re.findall("(\ \d+\ |\ \d+\ -\ )?(\ ova|\ oad|\ ona|\ OVA|\ OAD|\ ONA)(\ \d+|\ -\ \d+)?", r)
        ova = [''.join(o for o in ov).strip() for ov in ova]
        if len(ova) > 0:
            episode = max(ova, key=len)

    """ check if it is a special """
    if len(episode) < 1:
        special = re.findall("(\ sp\ |\ special\ )(\d+|-\ \d+)?", r, flags=re.IGNORECASE)
        special = [''.join(s for s in sp).strip() for sp in special]
        if len(special) > 0:
            episode = max(special, key=len)

    """ if it isn't an op/ed, ova/oad, or a special find the episode number """
    if len(episode) < 1:
        episode = re.findall( r'(episode\ \d+|ep\d+|e\d+|\ \d+)(\.\d)?(v\d+)?', r, flags=re.IGNORECASE ) 
        episode = [''.join(e for e in ep).strip() for ep in episode]
        if len(episode) == 1:
            episode = episode[0]
        elif len(episode) < 1:
            episode = None
        else:
            """ I am assuming that if there is more than one number the last is probably the episode """
            """ works for 2 out of 2 of my real world test cases """
            episode = episode[-1]
    
    # by now we know what the episode is or we know nothing
    d['episode_number'] = episode

    """ remove some things from the rest of the string """

    if episode is not None:
        r = r.split(episode)[0]

    r = r.split(" - ")[0]
    to_remove = ("BD", "bd", "Blu-ray", "blu-ray", "Bluray", "bluray", "TV", "tv")
    for thing in to_remove:
        if thing in r:
            r = r.replace(thing, "")

    d['anime_name'] = r.strip()

    return d


""" find the media filesize """
def get_filesize(path):
    return os.stat(path).st_size

""" find media file duration """
def get_duration(path):
    p = subprocess.Popen( DURATION.format(path), stdout=subprocess.PIPE, shell=True )
    out, err = p.communicate()
    return float(out.strip())


""" generate video thumbnail """
def get_thumbnail(path, duration):
    thumnail_name = "_".join( path.split("/")[-1].split(".")[0].split(" ") )
    subprocess.Popen(
        THUMB.format( duration/3, path, FOLDER, thumnail_name ), 
        stdout=FNULL, 
        stderr=subprocess.STDOUT, 
        shell=True
    )
    return "/media/videos/{}.jpg".format(thumnail_name)


""" check for the presence of subtitles """
def get_subtitles(path):
    b = subprocess.Popen(CHECK.format(path), shell=True, stdout=subprocess.PIPE)
    out, err = b.communicate()
    streams = []
    stream = {}
    try:
        for line in out.splitlines():
            line = line.decode()
            if line == "[STREAM]":
                stream = {}
            elif line == "[/STREAM]":
                streams.append(stream)
            else:
                if len(line.split("=")) == 2:
                    stream[line.split("=")[0]] = line.split("=")[1]
    except UnicodeDecodeError as e:
        print("some weird unicode error here:", e)
        print("caused by:", path)

    subtitles = [s for s in streams if s["codec_type"] == 'subtitle']

    subs = ""
    for i in range(len(subtitles)):
        try:
            subs += "index=" + subtitles[i]["index"] + ","
            subs += "codec=" + subtitles[i]["codec_name"] + ","
            subs += "language=" + subtitles[i]["TAG:language"]
            if i < len(subtitles) - 1:
                subs += ";"
        except KeyError:
            break

    return subs


""" Search the jikan api for anime information from MAL """
def search_jikan(anime):
    # all_results = session.get(SEARCH_URL.format(anime), verify=False).json()["result"]
    all_results = session.get(SEARCH_URL.format(anime)).json()["result"]
    titles = [result["title"].lower() for result in all_results]
    matches = difflib.get_close_matches(anime, titles, n=1, cutoff=0.5)
    entry = ""
    if len(matches) > 0:
        for result in all_results:
            if result["title"].lower() == matches[0]:
                entry = result
                break
    else:
        # fallback if the name doesn't match
        entry = all_results[0]
    return entry


""" save a thumbnail image for the anime from MAL """
def download_thumbnail(anime, url):
    thumbnail_name = "/media/anime/" + "_".join(anime.split(" ")) + ".jpg"
    r = session.get(url, stream=True)
    with open(os.getcwd() + thumbnail_name, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
    return thumbnail_name