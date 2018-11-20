import subprocess

DURATION = u'''ffprobe -i "{}" -show_entries format=duration -v quiet -of csv="p=0"'''


def get_duration(path):
    """ 
    finds media file duration 
    """   
    p = subprocess.Popen( DURATION.format(path), stdout=subprocess.PIPE, shell=True )
    out, err = p.communicate()
    return float(out.strip())