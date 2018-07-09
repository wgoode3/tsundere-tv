import subprocess, time

ENCODE = '''ffmpeg -re -i "{0}" -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -vf subtitles="{1}" -b:v 500k -minrate 500k -maxrate 500k -bufsize 1000k -s 640x360 -f flv rtmp://127.0.0.1/dash/{2}_low -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -vf subtitles="{1}" -b:v 1500k -minrate 1500k -maxrate 1500k -bufsize 3000k -s 1280x720 -f flv rtmp://127.0.0.1/dash/{2}_med -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -vf subtitles="{1}" -b:v 5000k -minrate 5000k -maxrate 5000k -bufsize 10000k -s 1920x1080 -f flv rtmp://127.0.0.1/dash/{2}_high'''

def escape_chars(string):
	s = ""
	for ltr in string:
		if ltr == "[" or ltr == "]":
			s += "\\"
		s += ltr
	return s

def play(path):
	key = path.split("/")[-1].split(".")[0]
	key = "_".join(key.split(" "))
	p = escape_chars(path)
	# k = escape_chars(key)
	# print "*"*100
	# print ENCODE.format(path, p, key)
	# print "*"*100
	subprocess.Popen(ENCODE.format(path, p, key), shell=True)

	# wait for the file to start encoding
	# hopefully this is long enough
	# time.sleep(10)
	return key
