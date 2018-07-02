import os

VIDEOS = [[]]
extensions = ("mkv", "avi", "ogm", "mp4", "webm")

def vid_search(loc):
	ls = os.listdir(loc)
	for thing in ls:
		if os.path.isdir(os.path.join(loc, thing)):
			if not thing.startswith("."):
				vid_search(os.path.join(loc, thing))
		elif os.path.isfile(os.path.join(loc, thing)):
			if thing.split(".")[-1] in extensions:
				VIDEOS[0].append(os.path.join(loc, thing))
	return VIDEOS[0]

# returns a list paths to all videos matching the allowed extensions
def start():
	VIDEOS[0] = []
	return vid_search(os.path.expanduser("~"))