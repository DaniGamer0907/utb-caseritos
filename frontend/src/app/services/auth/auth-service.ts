import { HttpClient, HttpHeaders } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { inject, Injectable, PLATFORM_ID, signal } from '@angular/core';
import { tap } from 'rxjs';
import { API_BASE_URL } from '../api/api-config';

interface LoginResponse {
  access_token: string;
  token_type: string;
  role: string;
  name: string;
}

interface JwtPayload {
  sub?: string;
  role?: string;
  exp?: number;
}

export interface AuthSession {
  token: string;
  role: string;
  email: string;
  name: string;
  exp: number;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly platformId = inject(PLATFORM_ID);
  private readonly url = `${API_BASE_URL}/auth`;
  readonly session = signal<AuthSession | null>(null);

  constructor() {
    this.restoreSession();
  }

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
        const exp = payload?.exp;
        const email = payload?.sub ?? user;

        if (!role || !exp || !email) {
          this.logout();
          return;
        }

        this.persistSession({
          token: response.access_token,
          role,
          email,
          name: response.name.trim() || email.split('@')[0],
          exp,
        });
      })
    );
  }

  registro(datosUsuario: any) {
    return this.http.post(`${this.url}/registro`, datosUsuario);
  }

  getRol(): string | null {
    return this.isLoggedIn() ? this.session()?.role ?? null : null;
  }

  getToken(): string | null {
    return this.isLoggedIn() ? this.session()?.token ?? null : null;
  }

  getUser() {
    const currentSession = this.session();
    if (!currentSession || !this.isLoggedIn()) {
      return null;
    }

    return {
      name: currentSession.name,
      email: currentSession.email,
      role: currentSession.role,
    };
  }

  isLoggedIn(): boolean {
    const currentSession = this.session();
    if (!currentSession) {
      return false;
    }

    if (Date.now() >= currentSession.exp * 1000) {
      this.logout();
      return false;
    }

    return true;
  }

  logout(): void {
    this.session.set(null);
    const storage = this.getStorage();
    if (!storage) {
      return;
    }

    storage.removeItem('token');
    storage.removeItem('role');
    storage.removeItem('userName');
  }

  private restoreSession(): void {
    const storage = this.getStorage();
    const token = storage?.getItem('token');

    if (!storage || !token) {
      this.session.set(null);
      return;
    }

    const payload = this.decodeToken(token);
    const role = payload?.role ?? storage.getItem('role');
    const email = payload?.sub;
    const exp = payload?.exp;

    if (!role || !email || !exp || Date.now() >= exp * 1000) {
      this.logout();
      return;
    }

    this.session.set({
      token,
      role,
      email,
      name: storage.getItem('userName') ?? email.split('@')[0],
      exp,
    });
  }

  private persistSession(session: AuthSession): void {
    const storage = this.getStorage();
    if (storage) {
      storage.setItem('token', session.token);
      storage.setItem('role', session.role);
      storage.setItem('userName', session.name);
    }

    this.session.set(session);
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
