import { Component, inject, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminService, Pedido } from '../../../services/admin/admin.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
})
export class DashboardComponent implements OnInit {
  private readonly adminService = inject(AdminService);

  pedidos    = signal<Pedido[]>([]);
  isLoading  = signal(true);
  error      = signal('');
  filtro     = signal('todos');

  totalPedidos  = computed(() => this.pedidos().length);
  enPreparacion = computed(() => this.pedidos().filter(p => p.estado === 'preparacion').length);
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
      pendiente:   'Pendiente',
      preparacion: 'En preparación',
      listo:       'Listo',
      entregado:   'Entregado',
    };
    return labels[estado] ?? estado;
  }
}