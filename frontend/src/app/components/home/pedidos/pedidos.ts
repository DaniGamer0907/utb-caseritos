import { CommonModule } from '@angular/common';
import { Component, effect, inject, signal } from '@angular/core';
import { AuthService } from '../../../services/auth/auth-service';
import { Pedido, PedidosService } from '../../../services/pedidos/pedidos-service';
import { Store } from '../../../services/status/store';

@Component({
  selector: 'app-pedidos',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './pedidos.html',
  styleUrl: './pedidos.css',
})
export class Pedidos {
  private readonly pedidosService = inject(PedidosService);
  private readonly authService = inject(AuthService);
  protected readonly store = inject(Store);

  readonly pedidos = signal<Pedido[]>([]);
  readonly isLoading = signal(false);
  readonly errorMessage = signal('');

  constructor() {
    effect(() => {
      const session = this.authService.session();
      this.pedidosService.refreshTick();
      if (!session) {
        this.pedidos.set([]);
        this.isLoading.set(false);
        this.errorMessage.set('');
        return;
      }

      this.loadPedidos();
    });
  }

  protected isLoggedIn(): boolean {
    return this.authService.isLoggedIn();
  }

  protected estadoLabel(estado: string): string {
    const labels: Record<string, string> = {
      pendiente: 'Pendiente',
      confirmado: 'Confirmado',
      entregado: 'Entregado',
      cancelado: 'Cancelado',
    };

    return labels[estado] ?? estado;
  }

  protected trackByPedidoId(_: number, pedido: Pedido): number {
    return pedido.id;
  }

  private loadPedidos(): void {
    this.isLoading.set(true);
    this.errorMessage.set('');

    this.pedidosService.listPedidos().subscribe({
      next: (pedidos) => {
        this.pedidos.set(
          [...pedidos].sort(
            (a, b) => new Date(b.fecha_creacion).getTime() - new Date(a.fecha_creacion).getTime()
          )
        );
        this.isLoading.set(false);
      },
      error: (error) => {
        if (error?.status === 404) {
          this.pedidos.set([]);
          this.errorMessage.set('');
          this.isLoading.set(false);
          return;
        }

        const detail =
          typeof error?.error?.detail === 'string'
            ? error.error.detail
            : 'No fue posible cargar tus pedidos.';

        this.pedidos.set([]);
        this.errorMessage.set(detail);
        this.isLoading.set(false);
      },
    });
  }
}
