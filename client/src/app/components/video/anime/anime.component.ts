import { Component, OnInit, Input  } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';

@Component({
  selector: 'app-anime',
  templateUrl: './anime.component.html',
  styleUrls: ['./anime.component.css']
})
export class AnimeComponent implements OnInit {

  constructor(private _router: Router) {
  }

  @Input() anime:any; 

  ngOnInit() {
  }

  info(){
    this._router.navigate([`/anime/${this.anime.id}`]);
  }

}
