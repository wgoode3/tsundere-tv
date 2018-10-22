import { Component, OnInit } from '@angular/core';
import { VideoService } from '../../../services/video.service';
import { ActivatedRoute, Params, Router } from '@angular/router';

@Component({
  selector: 'app-anime-single',
  templateUrl: './anime-single.component.html',
  styleUrls: ['./anime-single.component.css']
})
export class AnimeSingleComponent implements OnInit {

  anime: any;
  videos: [any];

  constructor(private _videoService:VideoService, private _route: ActivatedRoute, private _router: Router) {
  }

  ngOnInit() {
    this._route.params.subscribe((params: Params) => {
      this._videoService.getOne(params['id']).subscribe( data => {
        this.anime = data['anime'];
        this.videos = data['videos'];
      });
    });
  }

}
