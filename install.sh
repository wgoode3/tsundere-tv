#!/bin/bash

apt-get build-dep nginx
apt-get source nginx
git clone https://github.com/ut0mt8/nginx-rtmp-module/
cd nginx-1.10.3
./configure --add-module=../nginx-rtmp-module
make
make install
wget https://isrv.pw/html5-live-streaming-with-mpeg-dash/nginx.service.txt -O /lib/systemd/system/nginx.service
systemctl daemon-reload
systemctl enable nginx.service

cd ..
git clone https://github.com/wgoode3/video-server.git
cd video-server
cp nginx.conf /usr/local/nginx/conf/nginx.conf

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
