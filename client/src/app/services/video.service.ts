import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class VideoService {

  constructor(private _http: HttpClient){
  }

  getAll(){
    return this._http.get('/videos');
  }

  getOne(id){
    return this._http.get(`/videos/${id}`);
  }

  watch(id){
    return this._http.get(`/videos/${id}/watch`);
  }

  search(id){
    return this._http.get('/videos/search');
  }

}
