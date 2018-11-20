import subprocess

CHECK = u'''ffprobe -v error -show_entries stream '{}' '''


def get_subtitles(path):
    """ 
    checks for the presence of subtitles 
    """
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