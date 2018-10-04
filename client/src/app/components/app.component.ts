import { Component } from '@angular/core';
import { UserService } from '../services/user.service';
import { ActivatedRoute, Params, Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  
  title = 'tsundere.tv';
  user:any;

  constructor(private _userService:UserService, private _router: Router){
  }
  
  ngOnInit(){
    this.getUser();
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

}
