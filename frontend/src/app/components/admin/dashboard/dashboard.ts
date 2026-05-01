import { Component, inject, OnInit, signal, computed, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminService, Pedido } from '../../../services/admin/admin.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
  encapsulation: ViewEncapsulation.None,
})
export class DashboardComponent implements OnInit {
  private readonly adminService = inject(AdminService);

  pedidos   = signal<Pedido[]>([]);
  isLoading = signal(true);
  error     = signal('');
  filtro    = signal('todos');

  totalPedidos  = computed(() => this.pedidos().length);
  enPreparacion = computed(() => this.pedidos().filter(p => p.estado === 'en preparación').length);
  entregados    = computed(() => this.pedidos().filter(p => p.estado === 'entregado').length);
  pendientes    = computed(() => this.pedidos().filter(p => p.estado === 'pendiente').length);

  pedidosFiltrados = computed(() => {
    const f = this.filtro();
    return f === 'todos' ? this.pedidos() : this.pedidos().filter(p => p.estado === f);
  });

  ngOnInit(): void {
    this.adminService.listPedidos().subscribe({
      next: (data) => {
        this.pedidos.set(data);
        this.isLoading.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar los pedidos.');
        this.isLoading.set(false);
      },
    });
  }

  setFiltro(f: string): void {
    this.filtro.set(f);
  }

  estadoLabel(estado: string): string {
    const labels: Record<string, string> = {
      'pendiente':      'Pendiente',
      'en preparación': 'En preparación',
      'entregado':      'Entregado',
    };
    return labels[estado] ?? estado;
  }

  cambiarEstado(pedido: Pedido, nuevoEstado: string): void {
    this.adminService.actualizarEstadoPedido(pedido.id, nuevoEstado).subscribe({
      next: () => {
        this.pedidos.update(lista =>
          lista.map(p => p.id === pedido.id ? { ...p, estado: nuevoEstado } : p)
        );
      },
      error: () => {
        console.error('Error al actualizar el estado del pedido');
      }
    });
  }

  estadoClass(estado: string): string {
  const clases: Record<string, string> = {
    'pendiente':      'estado-pendiente',
    'en preparación': 'estado-preparacion',
    'entregado':      'estado-entregado',
  };
  return clases[estado] ?? '';
}
}