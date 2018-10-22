import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private _http: HttpClient){
  }
  
  allUsers(){
    return this._http.get('/api/user');
  }

  register(data){
    return this._http.post("/api/user", data);
  }

  login(data){
    return this._http.post('/api/user/session', data);
  }

  logout(){
    return this._http.delete('/api/user/session');
  }

  session(){
    return this._http.get('/api/user/session');
  }

  getOne(id){
    return this._http.get(`/api/user/${id}`);
  }

  update(id, data){
    return this._http.put(`/api/user/${id}`, data);
  }

  delete(id){
    return this._http.delete(`/api/user/${id}`);
  }
  
}
