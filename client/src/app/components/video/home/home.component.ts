import { Component, OnInit, OnDestroy } from '@angular/core';
import { VideoService } from '../../../services/video.service';
import { ActivatedRoute, Params, Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, OnDestroy {
  
  // https://stackoverflow.com/questions/40983055/how-to-reload-the-current-route-with-the-angular-2-router
  navigationSubscription;
  all_anime = [];

  constructor(private _videoService:VideoService, private _router: Router) {
    this.navigationSubscription = this._router.events.subscribe((e: any) => {
      if (e instanceof NavigationEnd) {
        this.ngOnInit();
      }
    });
  }

  ngOnInit() {
    this._videoService.getAll().subscribe( data => {
      this.all_anime = data['all_anime'];
    });
  }

  ngOnDestroy() {
    if (this.navigationSubscription) {
      this.navigationSubscription.unsubscribe();
    }
  }

}
