import os


def get_filesize(path):
    """ 
    finds the media filesize 
    """
    return os.stat(path).st_size