import { Component, OnInit, Input } from '@angular/core';
import { VideoService } from '../../../services/video.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-video',
  templateUrl: './video.component.html',
  styleUrls: ['./video.component.css']
})
export class VideoComponent implements OnInit {

  @Input() video: any;

  constructor(private _videoService: VideoService, private _router: Router) {
  }

  ngOnInit() {
    this.readable_filesize();
    this.readable_duration();
  }

  play(e){
    if(e.target.classList.contains("play")){
      e.target.parentNode.parentNode.classList.add("loading");
    }else{
      e.target.parentNode.classList.add("loading");
    }
    this._videoService.watch(this.video.id).subscribe( data => {
      console.log(data);
      localStorage.setItem("host", data['host']);
      localStorage.setItem("key", data['key']);
      localStorage.setItem("pid", data['pid']);
      localStorage.setItem('video_id', data['id']);
      localStorage.setItem('filename', data['video']['filename']);
      localStorage.setItem('thumb', data['video']['thumbnail']);
      let router = this._router;
      let vid_id = this.video.id;
      function fire_when_ready(){
        fetch(`http://${data['host']}/dash/${data['key']}.mpd`).then( res => {
          // console.log(res.status);
          if(res.status != 200){
            setTimeout(function(){fire_when_ready();}, 1000);
          }else{
            router.navigate([`/watch/${vid_id}`]);
          }
        });
      }
      fire_when_ready();
    });
  }

  readable_filesize(){
    let size = this.video.filesize;
    if (size < Math.pow(10, 3)) {
      this.video.filesize = `${size}B`;
    } else if (size < Math.pow(10, 6)) {
      this.video.filesize = `${size/1000>>0}KB`;
    } else if (size < Math.pow(10, 9)) {
      this.video.filesize = `${size/1000000>>0}MB`;
    } else {
      this.video.filesize = `${size/1000000000>>0}GB`;
    }
  }

  readable_duration(){
    let d = this.video.duration;
    let h = d/3600 >> 0;
    d %= 3600;
    let m = d/60 >> 0;
    d %= 60;
    this.video.duration = `${h}:${m}:${d>>0}`;
  }

}