import { Component, inject, OnInit, signal, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminService, Pago } from '../../../services/admin/admin.service';

@Component({
  selector: 'app-pagos',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './pagos.html',
  styleUrl: './pagos.css',
  encapsulation: ViewEncapsulation.None,
})
export class PagosComponent implements OnInit {
  private readonly adminService = inject(AdminService);

  pagos     = signal<Pago[]>([]);
  isLoading = signal(true);
  error     = signal('');

  ngOnInit(): void {
    this.adminService.listPagos().subscribe({
      next: (data) => {
        this.pagos.set(data);
        this.isLoading.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar los pagos.');
        this.isLoading.set(false);
      },
    });
  }
}