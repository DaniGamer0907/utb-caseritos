import { HttpClient, HttpHeaders } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { inject, Injectable, PLATFORM_ID } from '@angular/core';
import { tap } from 'rxjs';

interface LoginResponse {
  access_token: string;
  token_type: string;
  role: string;
}

interface JwtPayload {
  sub?: string;
  role?: string;
  exp?: number;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly platformId = inject(PLATFORM_ID);
  private readonly url = 'http://localhost:8000/auth';

  login(user: string, pass: string) {
    const body = new URLSearchParams();
    body.set('username', user);
    body.set('password', pass);

    const options = {
      headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')
    };

    return this.http.post<LoginResponse>(`${this.url}/login`, body.toString(), options).pipe(
      tap((response) => {
        const payload = this.decodeToken(response.access_token);
        const role = payload?.role ?? response.role;
        const storage = this.getStorage();

        if (!storage) {
          return;
        }

        storage.setItem('token', response.access_token);
        storage.setItem('role', role ?? '');
      })
    );
  }

  registro(datosUsuario: any) {
    return this.http.post(`${this.url}/registro`, datosUsuario);
  }

  getRol(): string | null {
    if (!this.isLoggedIn()) {
      return null;
    }

    return this.getStorage()?.getItem('role') ?? null;
  }

  isLoggedIn(): boolean {
    const token = this.getStorage()?.getItem('token');
    if (!token) {
      return false;
    }

    const payload = this.decodeToken(token);
    const exp = payload?.exp;

    if (!payload || !exp || Date.now() >= exp * 1000) {
      this.logout();
      return false;
    }

    return true;
  }

  logout(): void {
    const storage = this.getStorage();
    if (!storage) {
      return;
    }

    storage.removeItem('token');
    storage.removeItem('role');
  }

  private getStorage(): Storage | null {
    if (!isPlatformBrowser(this.platformId)) {
      return null;
    }

    return localStorage;
  }

  private decodeToken(token: string): JwtPayload | null {
    try {
      const payload = token.split('.')[1];
      if (!payload) {
        return null;
      }

      const normalizedPayload = payload.replace(/-/g, '+').replace(/_/g, '/');
      const decodedPayload = atob(normalizedPayload);
      return JSON.parse(decodedPayload) as JwtPayload;
    } catch {
      return null;
    }
  }
}
