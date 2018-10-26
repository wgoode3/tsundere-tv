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

  constructor(private _videoService: VideoService) {
  }

  ngOnInit() {
    this.host = localStorage.getItem("host");
    this.key = localStorage.getItem("key");
    this.pid = localStorage.getItem("pid");
    this.filename = localStorage.getItem("filename");
    this.thumb = localStorage.getItem("thumb");
  }

  ngOnDestroy(){
    localStorage.clear();
    this._videoService.stop(this.pid).subscribe( data => {
      console.log(`we're leaving now! ${this.pid}`, data);
    });
  }

}
