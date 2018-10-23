import { Component, OnInit, Input } from '@angular/core';
import { VideoService } from '../../../services/video.service';

@Component({
  selector: 'app-video',
  templateUrl: './video.component.html',
  styleUrls: ['./video.component.css']
})
export class VideoComponent implements OnInit {

  @Input() video: any;

  constructor(private _videoService: VideoService) {
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