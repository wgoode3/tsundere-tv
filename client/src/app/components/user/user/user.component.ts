import { Component, OnInit } from '@angular/core';
import { UserService } from '../../../services/user.service';
import { ActivatedRoute, Params, Router } from '@angular/router';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {

  user: any;
  errors = {};
  avatar: {image: "", filename: ""};

  constructor(private _userService: UserService, private _route: ActivatedRoute, private _router: Router) {
  }

  ngOnInit() {
    this._route.params.subscribe((params: Params) => {
      this._userService.getOne(params['id']).subscribe( data => {
        this.user = data['user'];
        this.user['password'] = '';
      });
    });
  }

  changeAvatar(event){
    let _this = this;
    let file = event.target.files[0]
    let reader = new FileReader();
    reader.addEventListener("load", function() {
      _this.user['filename'] = file.name;
      _this.user['image'] = reader.result
      _this._userService.update(_this.user.id, _this.user).subscribe( data => {
        _this.ngOnInit();
        _this._router.navigate([`/user/${_this.user.id}`]);
      });
    }, false);
    if (file) {
      reader.readAsDataURL(file);
    }
  }

  update(id){
    this._userService.update(this.user.id, this.user).subscribe( data => {
      this.ngOnInit();
      this._router.navigate([`/user/${this.user.id}`]);
    });
  }

}
