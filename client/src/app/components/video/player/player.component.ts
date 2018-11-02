import { Component, OnInit, OnDestroy } from '@angular/core';
import { VideoService } from '../../../services/video.service';

@Component({
  selector: 'app-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.css']
})
export class PlayerComponent implements OnInit, OnDestroy {

  host;
  key;
  pid;
  filename;
  thumb;
  player;
  active;
  src;

  constructor(private _videoService: VideoService) {
  }

  ngOnInit() {
    this.host = localStorage.getItem("host");
    this.key = localStorage.getItem("key");
    this.pid = localStorage.getItem("pid");
    this.filename = localStorage.getItem("filename");
    this.thumb = localStorage.getItem("thumb");
    this.active = true;
    if (window['MediaSource']){
      this.src = `http://${this.host}/dash/${this.key}.mpd`;
    } else {
      this.src = `http://${this.host}/hls/${this.key}.m3u8`;
      this.active = false;
    }
    this.loadVideo();
    this.inactivityTime();
    window['garden'] = false;
  }
  
  loadVideo(){
    let player = window['dashjs'].MediaPlayer().create();
    let vid = document.getElementById("vid");
    let url;
    if (window['MediaSource']) {
      url = `http://${this.host}/dash/${this.key}.mpd`;
      player.initialize(vid, url, true);
      player.setFastSwitchEnabled(true);
    } else {
      url = `http://${this.host}/hls/${this.key}.m3u8`;
      vid['src'] = url;
      player.initialize(vid, url, true);
      player.setFastSwitchEnabled(true);
      player.reset();
    }
    this.player = player;
  }

  ngOnDestroy(){
    localStorage.clear();
    this._videoService.stop(this.pid).subscribe( data => {
      console.log(`we're leaving now! ${this.player.time()}`, data);
    });
    this.active = false;
    window['garden'] = true; 
  }

  inactivityTime() {
    let t;
    let _this = this;

    let hidenav = function() {
      if(_this.active){
        document.getElementById("nav").style.opacity = '0';
        document.querySelector("body").style.cursor = "none";
      }
    }

    let resetTimer = function() {
      if(_this.active){
        document.getElementById("nav").style.opacity = '1';
        document.querySelector("body").style.cursor = "auto";
        clearTimeout(t);
        t = setTimeout(hidenav, 3000)
      }
    }
    window.onload = resetTimer;
    document.onmousemove = resetTimer;
    document.onkeypress = resetTimer;
  }

}
