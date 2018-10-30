#!/bin/bash
echo "installing nginx with rtmp"

# this sometimes has issues...
apt-get build-dep nginx

git clone https://github.com/ut0mt8/nginx-rtmp-module/

apt-get source nginx
# cd into whatever version of nginx we downloaded (1.14 as of 10/30/2018)
cd nginx-1.*
./configure --add-module=../nginx-rtmp-module
make
make install

echo "[Unit]
Description=A high performance web server and a reverse proxy server
After=network.target

[Service]
Type=forking
PIDFile=/run/nginx.pid
ExecStartPre=/usr/local/nginx/sbin/nginx -t -q -g 'daemon on; master_process on;'
ExecStart=/usr/local/nginx/sbin/nginx -g 'daemon on; master_process on;'
ExecReload=/usr/local/nginx/sbin/nginx -g 'daemon on; master_process on;' -s reload
ExecStop=-/sbin/start-stop-daemon --quiet --stop --retry QUIT/5 --pidfile /run/nginx.pid
TimeoutStopSec=5
KillMode=mixed

[Install]
WantedBy=multi-user.target" > /lib/systemd/system/nginx.service

systemctl daemon-reload
systemctl enable nginx.service

# we can do some cleaning up after ourselves
cd ..
rm -rf nginx-*
rm -rf nginx_*

# we may want to edit this file first
cp nginx.conf /usr/local/nginx/conf/nginx.conf

echo "done"