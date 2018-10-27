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

  constructor(private _videoService: VideoService) {
  }

  ngOnInit() {
    this.host = localStorage.getItem("host");
    this.key = localStorage.getItem("key");
    this.pid = localStorage.getItem("pid");
    this.filename = localStorage.getItem("filename");
    this.thumb = localStorage.getItem("thumb");
    this.loadVideo();
  }

  loadVideo(){
    let vid = document.getElementById("vid");
    let player = window['dashjs'].MediaPlayer().create();
    let url = `http://${this.host}/dash/${this.key}.mpd`;
    console.log("initializing...", vid, url, player);
    player.initialize(vid, url, true);
    player.setFastSwitchEnabled(true);
    this.player = player;
  }

  ngOnDestroy(){
    localStorage.clear();
    this._videoService.stop(this.pid).subscribe( data => {
      console.log(`we're leaving now! ${this.player.time()}`, data);
    });
  }

}
