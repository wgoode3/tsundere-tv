# tsundere-tv

<img src="https://github.com/wgoode3/tsundere-tv/blob/master/demo.gif?raw=true" alt="demo.gif" />

``` 
"It's not like I want to host your anime, baka~!" 
```

Home anime media server in the style of Plex, recursively searches for, categorizes, and displays media on the host system for transcoding and streaming to a web client. 

<hr>

### Technologies used: 
* Python
* Django
* Angular
* [nginx-rtmp-module](https://github.com/ut0mt8/nginx-rtmp-module)
* FFmpeg
* [MPEG-DASH (dash.js)](https://github.com/Dash-Industry-Forum/dash.js)
* [Jikan API](https://github.com/jikan-me/jikan)

<hr>

### Deploy/Testing instructions
0. Insure the following are installed
    * git
    * FFmpeg
    * Python 3.5+
    * virtualenv
    * Node 8.10+
    * Angular CLI 6+

1. Clone this repository
```shell
$ git clone https://github.com/wgoode3/tsundere-tv.git
```

2. Run the install script
```shell
$ sudo chmod +x install.sh
$ ./install.sh
```

3. Build the client code
```shell
$ cd client
$ npm i
$ ng build
$ # use ng build --prod for production
```

4. Run the run script
```shell
$ sudo chmod +x run.sh
$ ./run.sh
```