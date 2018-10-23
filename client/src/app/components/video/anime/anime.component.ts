import { Component, OnInit, Input  } from '@angular/core';

@Component({
  selector: 'app-anime',
  templateUrl: './anime.component.html',
  styleUrls: ['./anime.component.css']
})
export class AnimeComponent implements OnInit {

  constructor() {
  }

  @Input() anime:any; 

  ngOnInit() {
  }

}
