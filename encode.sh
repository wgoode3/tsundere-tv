#!/bin/bash

# ffmpeg -re -i "media/example.mkv" -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset fast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -vf subtitles="media/example.mkv" -b:v 2000k -minrate 2000k -maxrate 2000k -bufsize 4000k -s 1280x720 -f flv "source/test.mpd" -y

# ffmpeg -re -i "media/example.mkv" \
# -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset fast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -vf subtitles="media/example.mkv" -b:v 2000k -minrate 2000k -maxrate 2000k -bufsize 4000k -s 1280x720 -f flv "rtmp://192.168.1.141/dash/test" -y \
# -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset fast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -vf subtitles="media/example.mkv" -b:v 2000k -minrate 2000k -maxrate 2000k -bufsize 4000k -s 1280x720 -f flv "source/test.mpd" -y

# ffmpeg -re -i "media/example.mkv" -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset fast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -vf subtitles="media/example.mkv" -b:v 2000k -minrate 2000k -maxrate 2000k -bufsize 4000k -s 1280x720 -f flv "rtmp://127.0.0.1/dash/test_med"

# ffmpeg -re -i "media/example.mkv" \
#     -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -vf subtitles="media/example.mkv" -b:v 500k -minrate 500k -maxrate 500k -bufsize 1000k -s 640x360 -f flv rtmp://127.0.0.1/dash/test_low \
#     -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -vf subtitles="media/example.mkv" -b:v 1500k -minrate 1500k -maxrate 1500k -bufsize 3000k -s 1280x720 -f flv rtmp://127.0.0.1/dash/test_med \
#     -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -vf subtitles="media/example.mkv" -b:v 5000k -minrate 5000k -maxrate 5000k -bufsize 10000k -s 1920x1080 -f flv rtmp://127.0.0.1/dash/test_high

# ffmpeg -re -i "media/[Mazui]_Spice_and_Wolf_II_-_special_1_[7F7C59BC].mkv" \
#     -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -b:v 500k -minrate 500k -maxrate 500k -bufsize 1000k -s 640x360 -f flv rtmp://127.0.0.1/dash/test_low \
#     -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -b:v 1500k -minrate 1500k -maxrate 1500k -bufsize 3000k -s 1280x720 -f flv rtmp://127.0.0.1/dash/test_med \
#     -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -b:v 5000k -minrate 5000k -maxrate 5000k -bufsize 10000k -s 1920x1080 -f flv rtmp://127.0.0.1/dash/test_high

   
ffmpeg -re -i "media/[Mazui]_Spice_and_Wolf_II_-_special_2_[C56C41F8].mkv" \
    -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -b:v 500k -minrate 500k -maxrate 500k -bufsize 1000k -s 640x360 -f flv rtmp://127.0.0.1/dash/test_low \
    -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -b:v 1500k -minrate 1500k -maxrate 1500k -bufsize 3000k -s 1280x720 -f flv rtmp://127.0.0.1/dash/test_med \
    -c:a aac -ac 2 -b:a 128k -strict -2 -c:v libx264 -pix_fmt yuv420p -profile:v baseline -preset ultrafast -tune zerolatency -vsync cfr -x264-params "nal-hrd=cbr" -b:v 5000k -minrate 5000k -maxrate 5000k -bufsize 10000k -s 1920x1080 -f flv rtmp://127.0.0.1/dash/test_high