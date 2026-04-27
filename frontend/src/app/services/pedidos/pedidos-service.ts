import { HttpClient, HttpHeaders } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { inject, Injectable, PLATFORM_ID } from '@angular/core';
import { forkJoin, map, Observable, of, switchMap } from 'rxjs';

export interface PedidoPayload {
  fecha_creacion?: string;
  estado: string;
  sugerencia: string;
}

export interface DetallePedidoPayload {
  pedidoid: number;
  proteinaid: number;
  tipalmuerzoid: number;
  cantidad: number;
  precio_unitario: number;
  total: number;
}

export interface ApiMessageResponse {
  mensaje: string;
  id?: number;
}

@Injectable({
  providedIn: 'root',
})
export class PedidosService {
  private readonly http = inject(HttpClient);
  private readonly platformId = inject(PLATFORM_ID);
  private readonly apiUrl = 'http://localhost:8000';

  crearPedido(payload: PedidoPayload): Observable<ApiMessageResponse> {
    return this.http.post<ApiMessageResponse>(
      `${this.apiUrl}/pedido/crearPedido`,
      payload,
      { headers: this.buildHeaders() }
    );
  }

  crearDetallePedido(payload: DetallePedidoPayload): Observable<ApiMessageResponse> {
    return this.http.post<ApiMessageResponse>(
      `${this.apiUrl}/detallesPedido/crearDetallesPedido`,
      payload,
      { headers: this.buildHeaders() }
    );
  }

  crearPedidoConDetalles(
    pedido: PedidoPayload,
    detalles: Omit<DetallePedidoPayload, 'pedidoid'>[]
  ): Observable<{ pedido: ApiMessageResponse; detalles: ApiMessageResponse[] }> {
    return this.crearPedido(pedido).pipe(
      switchMap((pedidoResponse) => {
        const pedidoid = pedidoResponse.id;
        if (!pedidoid) {
          throw new Error('No se recibió el ID del pedido');
        }

        if (!detalles.length) {
          return of({ pedido: pedidoResponse, detalles: [] });
        }

        const detallesCompletos: DetallePedidoPayload[] = detalles.map(d => ({
          ...d,
          pedidoid
        }));

        return forkJoin(detallesCompletos.map((detalle) => this.crearDetallePedido(detalle))).pipe(
          map((detalleResponses) => ({
            pedido: pedidoResponse,
            detalles: detalleResponses,
          }))
        );
      })
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
