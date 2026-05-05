import { HttpClient, HttpHeaders } from '@angular/common/http';
import { inject, Injectable, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { Observable } from 'rxjs';
import { API_BASE_URL } from '../api/api-config';

// ── Interfaces ────────────────────────────────────────────────────────────────

export interface Proteina {
  id: number;
  nombre: string;
  avaliable: number; // 0 = no disponible, 1 = disponible
}

export interface ProteinaPayload {
  nombre: string;
  avaliable: number;
}

export interface TipoAlmuerzo {
  id: number;
  nombre: string;
  descripcion: string;
  precio: number;
}

export interface TipoAlmuerzoPayload {
  nombre: string;
  descripcion: string;
  precio: number;
}

export interface Pago {
  id: number;
  metodopago: string;
  diadelpago: string;
  monto: number;
  referencia?: string;
  estado:string;
}

export interface Pedido {
  id: number;
  fecha_creacion: string;
  estado: string;
  sugerencia: string;
  total: number;
  pago_id?: number;
  usuario_id: number;
  nombre_usuario?:string;
}

export interface ApiResponse {
  mensaje: string;
  id?: number;
}

// ── Servicio ──────────────────────────────────────────────────────────────────

@Injectable({ providedIn: 'root' })
export class AdminService {
  private readonly http       = inject(HttpClient);
  private readonly platformId = inject(PLATFORM_ID);
  private readonly apiUrl     = API_BASE_URL;

  // ── PROTEÍNAS ──────────────────────────────────────────────────────────────

  listProteinas(): Observable<Proteina[]> {
    return this.http.get<Proteina[]>(`${this.apiUrl}/proteina/listProteinas`);
  }

  crearProteina(payload: ProteinaPayload): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(
      `${this.apiUrl}/proteina/crearProteina`,
      payload,
      { headers: this.buildHeaders() }
    );
  }

  actualizarEstadoPago(id: number, estado: string) {
  return this.http.patch(
    `${this.apiUrl}/Pago/actualizarEstado?id=${id}&estado=${encodeURIComponent(estado)}`,
    {},
    { headers: this.buildHeaders() }
  );
}
  
  actualizarEstadoPedido(id: number, estado: string): Observable<ApiResponse> {
    return this.http.patch<ApiResponse>(
      `${this.apiUrl}/pedido/actualizarEstado?id=${id}&estado=${encodeURIComponent(estado)}`,
      {},
      { headers: this.buildHeaders() }
    );
  }

  actualizarProteina(id: number, payload: ProteinaPayload): Observable<ApiResponse> {
    return this.http.put<ApiResponse>(
      `${this.apiUrl}/proteina/actualizarProteina?id=${id}`,
      payload,
      { headers: this.buildHeaders() }
    );
  }

  eliminarProteina(id: number): Observable<ApiResponse> {
    return this.http.delete<ApiResponse>(
      `${this.apiUrl}/proteina/borrarProteina?id=${id}`,
      { headers: this.buildHeaders() }
    );
  }

  // ── ALMUERZOS ─────────────────────────────────────────────────────────────

  listAlmuerzos(): Observable<TipoAlmuerzo[]> {
    return this.http.get<TipoAlmuerzo[]>(`${this.apiUrl}/tipoalmuerzo/listTiposAlmuerzo`);
  }

  crearAlmuerzo(payload: TipoAlmuerzoPayload): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(
      `${this.apiUrl}/tipoalmuerzo/crearTipoAlmuerzo`,
      payload,
      { headers: this.buildHeaders() }
    );
  }

  actualizarAlmuerzo(id: number, payload: TipoAlmuerzoPayload): Observable<ApiResponse> {
    return this.http.put<ApiResponse>(
      `${this.apiUrl}/tipoalmuerzo/actualizarTipoAlmuerzo?id=${id}`,
      payload,
      { headers: this.buildHeaders() }
    );
  }

  eliminarAlmuerzo(id: number): Observable<ApiResponse> {
    return this.http.delete<ApiResponse>(
      `${this.apiUrl}/tipoalmuerzo/borrarTipoAlmuerzo?id=${id}`,
      { headers: this.buildHeaders() }
    );
  }

  // ── PAGOS ─────────────────────────────────────────────────────────────────

  listPagos(): Observable<Pago[]> {
    return this.http.get<Pago[]>(
      `${this.apiUrl}/Pago/listPagos`,
      { headers: this.buildHeaders() }
    );
  }

  // ── PEDIDOS ───────────────────────────────────────────────────────────────

  listPedidos(): Observable<Pedido[]> {
    return this.http.get<Pedido[]>(
      `${this.apiUrl}/pedido/listPedidos`,
      { headers: this.buildHeaders() }
    );
  }

  // ── HEADERS ───────────────────────────────────────────────────────────────

  private buildHeaders(): HttpHeaders {
    const token = isPlatformBrowser(this.platformId)
      ? localStorage.getItem('token')
      : null;

    let headers = new HttpHeaders().set('Content-Type', 'application/json');
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }
    return headers;
  }
}