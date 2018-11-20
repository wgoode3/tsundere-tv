import subprocess

def stop_transcoding(pid):
    """ 
    stops the transcoding process
    """
    subprocess.Popen("kill {pid}".format(pid=pid), shell=True)