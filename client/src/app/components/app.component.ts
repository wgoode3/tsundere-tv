import { Component, OnInit, OnDestroy } from '@angular/core';
import { UserService } from '../services/user.service';
import { VideoService } from '../services/video.service';
import { ActivatedRoute, Params, Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {

  navigationSubscription;
  title = 'tsundere.tv';
  user:any;

  constructor(private _userService:UserService, private _videoService:VideoService, private _router: Router){
    this.navigationSubscription = this._router.events.subscribe((e: any) => {
      if (e instanceof NavigationEnd) {
        this.ngOnInit();
      }
    });
  }
  
  ngOnInit(){
    this.getUser();
  }

  ngOnDestroy() {
    if (this.navigationSubscription) {
      this.navigationSubscription.unsubscribe();
    }
  }
  
  onActivate(event){
    if(event.constructor.name == "HomeComponent"){
      this.getUser();
    }
  }

  getUser(){
    this._userService.session().subscribe( data => {
      if(data['user_id']){
        this._userService.getOne(data['user_id']).subscribe( data => {
          this.user = data['user'];
        });
      }
    });
  }

  logout(){
    this._userService.logout().subscribe( data => {
      this.user = null;
      this._router.navigate(['/']);
    });
  }

  search(){
    console.log("searching...");
    this._videoService.search().subscribe( data => {
      console.log(data);
      this._router.navigate(['/']);
    });
  }

  reset(){
    console.log("resetting...");
    this._videoService.reset().subscribe( data => {
      console.log(data);
      this._router.navigate(['/']);
    });
  }

}
