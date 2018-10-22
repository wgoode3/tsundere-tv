import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class VideoService {

  constructor(private _http: HttpClient){
  }

  getAll(){
    return this._http.get('/api/videos');
  }

  getOne(id){
    return this._http.get(`/api/videos/${id}`);
  }

  watch(id){
    return this._http.get(`/api/videos/${id}/watch`);
  }

  search(){
    return this._http.get('/api/videos/search');
  }

  reset(){
    return this._http.get('/api/videos/reset');
  }

}
