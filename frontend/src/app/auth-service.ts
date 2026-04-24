import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  url = "http://localhost:8000/auth"

  constructor (private http: HttpClient) {}

  login(user: string, pass: string) {
    const body = {
      email: user,
      password: pass
    };


    return this.http.post(`${this.url}/login`, body);
  }

  registro(datosUsuario: any){
    return this.http.post(`${this.url}/registro`, datosUsuario)
  }



}
