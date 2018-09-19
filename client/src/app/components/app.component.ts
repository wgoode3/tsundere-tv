import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'tsundere.tv';


  constructor(){
  }

  ngOnInit(){
    // localStorage.setItem("example", "this is an example");
    // localStorage.clear();
    // console.log(localStorage.getItem("example"));
  }

}
