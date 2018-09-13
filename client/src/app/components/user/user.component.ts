import { Component, OnInit, Input } from '@angular/core';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {

  @Input() user: any;
  avatar: {image: "", filename: ""};

  constructor(private _userService: UserService) { }

  ngOnInit() {
  }

  changeAvatar(event){
    let _this = this;
    let file = event.target.files[0]
    let reader = new FileReader();
    reader.addEventListener("load", function() {
      _this.user['filename'] = file.name;
      _this.user['image'] = reader.result
      _this._userService.update(_this.user.id, _this.user).subscribe( data => {
        _this._userService.getOne(_this.user.id).subscribe( data => {
          _this.user = data['user'];
        })
      })
    }, false);
    if (file) {
      reader.readAsDataURL(file);
    }
  }

}
