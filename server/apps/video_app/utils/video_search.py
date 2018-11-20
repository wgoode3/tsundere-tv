import os

VIDEOS = [[]]

# TODO: make both of these variables configurable by users
ALLOWED_EXTENSIONS = ( "mkv" )
MEDIA_PATHS = [ os.path.expanduser( "~" ) ]

def search( loc ):
    """ 
    finds media files to manage 
    """
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
    for path in MEDIA_PATHS:
        # may have to do some deduplication if users provide overlapping folders
        search( path )
    return VIDEOS[0]