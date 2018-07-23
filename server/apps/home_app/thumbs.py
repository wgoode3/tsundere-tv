import os, subprocess

THUMB = '''ffmpeg -ss {0} -i "{1}" -vframes 1 -s 480x270 "{2}/{3}.jpg" -y'''
DURATION = '''ffprobe -i "{}" -show_entries format=duration -v quiet -of csv="p=0"'''
FNULL = open(os.devnull, 'w')
FOLDER = os.getcwd() + "/apps/home_app/static/home_app/img"

def thumbify(file):
	p = subprocess.Popen(DURATION.format(file), stdout=subprocess.PIPE, shell=True)
	out, err = p.communicate()
	# print(file, out, err)
	duration = out.strip()
	dur = float(duration)/3
	name = "_".join(file.split("/")[-1].split(".")[0].split(" "))
	# print(THUMB.format(duration, file, FOLDER, name))
	subprocess.call(THUMB.format(dur, file, FOLDER, name), stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
	return {
		'duration': duration, 
		'thumb': name
	}