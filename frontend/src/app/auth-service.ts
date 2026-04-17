import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  url = "http://localhost:8000/auth"

  constructor (private http: HttpClient) {}

  login(user: string, pass: string) {
    const body = new URLSearchParams();
    body.set('username', user);
    body.set('password', pass);

    const options = {
      headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')
    };

    return this.http.post(`${this.url}/login`, body.toString(), options);
  }

  registro(datosUsuario: any){
    return this.http.post(`${this.url}/registro`, datosUsuario)
  }



}
