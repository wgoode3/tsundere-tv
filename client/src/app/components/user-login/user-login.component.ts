import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { ActivatedRoute, Params, Router } from '@angular/router';

@Component({
  selector: 'app-user-login',
  templateUrl: './user-login.component.html',
  styleUrls: ['./user-login.component.css']
})
export class UserLoginComponent implements OnInit {

  users = [];
  user = {};
  userSelected = false;
  password = "";
  errors = {};

  constructor(private _userService:UserService, private _router: Router) {
  }

  ngOnInit() {
    this._userService.allUsers().subscribe( data => {
      this.users = data['users'];
    });
  }

  newUser() {
    this._router.navigate(['/user/new']);
  }

  select(user, event){
    let boxUsers:any = document.getElementsByClassName('user');
    for(let u of boxUsers){
      u.classList.remove("selected");
    }
    let e = event.target;
    while(!e.classList.contains("user")){
      e = e.parentNode;
    }
    e.classList.add("selected");
    this.userSelected = true;
    this.user = user;
  }

  login(){
    this._userService.login({id: this.user['id'], password: this.password}).subscribe( data => {
      if(data['errors']){
        this.errors = data['errors'];
      }else{
        this._router.navigate(['/']);
      }
    });
  }

}
