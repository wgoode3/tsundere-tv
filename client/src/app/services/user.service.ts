import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private _http: HttpClient){
  }
  
  allUsers(){
    return this._http.get('/user');
  }

  register(data){
    return this._http.post("/user", data);
  }

  login(data){
    return this._http.post('/user/session', data);
  }

  logout(){
    return this._http.delete('/user/session');
  }

  session(){
    return this._http.get('/user/session');
  }

  getOne(id){
    return this._http.get(`/user/${id}`);
  }

  update(id, data){
    return this._http.put(`/user/${id}`, data);
  }

  delete(id){
    return this._http.delete(`/user/${id}`);
  }
  
}
