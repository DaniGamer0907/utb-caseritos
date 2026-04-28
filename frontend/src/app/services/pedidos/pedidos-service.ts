import { HttpClient, HttpHeaders } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { inject, Injectable, PLATFORM_ID } from '@angular/core';
import { Observable } from 'rxjs';
import { API_BASE_URL } from '../api/api-config';

export interface PedidoPayload {
  fecha_creacion?: string;
  estado: string;
  sugerencia: string;
  total: number;
  pago_id?: number;
}

export interface DetallePedidoPayload {
  pedidoid: number;
  proteinaid: number;
  tipalmuerzoid: number;
  cantidad: number;
  precio_unitario: number;
  total: number;
}

export interface PagoPayload {
  metodopago: string;
  diadelpago: string;
  monto: number;
  referencia?: string;
}

export interface CheckoutPagoPayload {
  metodopago: string;
  diadelpago: string;
  referencia?: string;
}

export interface CheckoutDetallePayload {
  proteinaid: number;
  tipalmuerzoid: number;
  cantidad: number;
}

export interface CheckoutPayload {
  sugerencia?: string;
  pago: CheckoutPagoPayload;
  detalles: CheckoutDetallePayload[];
}

export interface ApiMessageResponse {
  mensaje: string;
  id?: number;
  total?: number;
}

@Injectable({
  providedIn: 'root',
})
export class PedidosService {
  private readonly http = inject(HttpClient);
  private readonly platformId = inject(PLATFORM_ID);
  private readonly apiUrl = API_BASE_URL;

  crearPedido(payload: CheckoutPayload): Observable<ApiMessageResponse> {
    return this.http.post<ApiMessageResponse>(
      `${this.apiUrl}/pedido/crearPedido`,
      payload,
      { headers: this.buildHeaders() }
    );
  }

  actualizarPedido(id: number, payload: PedidoPayload): Observable<ApiMessageResponse> {
    return this.http.put<ApiMessageResponse>(
      `${this.apiUrl}/pedido/actualizarPedido?id=${id}`,
      payload,
      { headers: this.buildHeaders() }
    );
  }

  private buildHeaders(): HttpHeaders {
    const token = this.getStorage()?.getItem('token');
    let headers = new HttpHeaders().set('Content-Type', 'application/json');

    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }

    return headers;
  }

  private getStorage(): Storage | null {
    if (!isPlatformBrowser(this.platformId)) {
      return null;
    }

    return localStorage;
  }
}
