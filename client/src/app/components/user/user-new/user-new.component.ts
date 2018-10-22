import { Component, OnInit } from '@angular/core';
import { UserService } from '../../../services/user.service';
import { ActivatedRoute, Params, Router } from '@angular/router';

@Component({
  selector: 'app-user-new',
  templateUrl: './user-new.component.html',
  styleUrls: ['./user-new.component.css']
})
export class UserNewComponent implements OnInit {

  user = {username: '', email: '', password: '', confirm: ''};
  users = [];
  errors = {};

  constructor(private _userService:UserService, private _router: Router){
  }

  ngOnInit(){
    this._userService.allUsers().subscribe( data => {
      this.users = data['users'];
    });
  }

  register(){
    this._userService.register(this.user).subscribe( data => {
      console.log("This is what we get back", data);
      if(data['errors']){
        this.errors = data['errors'];
      }else{
        this._router.navigate(['/']);
      }
    });
  }

}
