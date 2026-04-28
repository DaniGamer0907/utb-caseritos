import { HttpClient, HttpHeaders } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { inject, Injectable, PLATFORM_ID } from '@angular/core';
import { forkJoin, map, Observable, of, switchMap } from 'rxjs';
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
  diadelpago: string; // ISO date string (YYYY-MM-DD)
  monto: number;
  referencia?: string;
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
  private readonly apiUrl = API_BASE_URL;

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

  crearPago(payload: PagoPayload): Observable<ApiMessageResponse> {
    return this.http.post<ApiMessageResponse>(
      `${this.apiUrl}/Pago/crearPago`,
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

  crearPedidoConDetalles(
    pedido: PedidoPayload,
    detalles: Omit<DetallePedidoPayload, 'pedidoid'>[],
    pago?: PagoPayload
  ): Observable<{ pedido: ApiMessageResponse; detalles: ApiMessageResponse[]; pago?: ApiMessageResponse }> {
    // 1. Crear el pago si existe
    const pagoObs: Observable<ApiMessageResponse | undefined> = pago ? this.crearPago(pago) : of(undefined);

    return pagoObs.pipe(
      switchMap((pagoResponse) => {
        // 2. Crear el pedido con el pago_id si corresponde
        const pedidoPayload = {
          ...pedido,
          pago_id: pagoResponse?.id
        };

        return this.crearPedido(pedidoPayload).pipe(
          switchMap((pedidoResponse) => {
            const pedidoid = pedidoResponse.id;
            if (!pedidoid) {
              throw new Error('No se recibió el ID del pedido');
            }

            // 3. Crear los detalles
            if (!detalles.length) {
              return of({ pedido: pedidoResponse, detalles: [], pago: pagoResponse });
            }

            const detallesCompletos: DetallePedidoPayload[] = detalles.map(d => ({
              ...d,
              pedidoid
            }));

            return forkJoin(detallesCompletos.map((detalle) => this.crearDetallePedido(detalle))).pipe(
              map((detalleResponses) => ({
                pedido: pedidoResponse,
                detalles: detalleResponses,
                pago: pagoResponse
              }))
            );
          })
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
