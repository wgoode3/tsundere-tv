import subprocess

ENCODE = '''ffmpeg -re -i "{0}" -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -b:v 500k -minrate 500k -maxrate 500k -bufsize 1000k -s 640x360 -f flv rtmp://127.0.0.1/dash/{1}_low -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -b:v 1500k -minrate 1500k -maxrate 1500k -bufsize 3000k -s 1280x720 -f flv rtmp://127.0.0.1/dash/{1}_med -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -b:v 5000k -minrate 5000k -maxrate 5000k -bufsize 10000k -s 1920x1080 -f flv rtmp://127.0.0.1/dash/{1}_high'''

def play(path):
	key = path.split("/")[-1].split(".")[0]
	print ENCODE.format(path, key)
	subprocess.Popen(ENCODE.format(path, key), shell=True)
	return key