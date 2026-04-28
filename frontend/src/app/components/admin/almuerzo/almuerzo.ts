import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService, TipoAlmuerzo, TipoAlmuerzoPayload } from '../../../services/admin/admin.service';

@Component({
  selector: 'app-almuerzo',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './almuerzo.html',
})
export class AlmuerzoComponent implements OnInit {
  private readonly adminService = inject(AdminService);

  almuerzos  = signal<TipoAlmuerzo[]>([]);
  isLoading  = signal(true);
  isSaving   = signal(false);
  error      = signal('');
  exito      = signal('');

  modoFormulario: 'crear' | 'editar' = 'crear';
  almuerzoSeleccionado: TipoAlmuerzo | null = null;
  form: TipoAlmuerzoPayload = { nombre: '', descripcion: '', precio: 0 };

  ngOnInit(): void {
    this.cargarAlmuerzos();
  }

  private cargarAlmuerzos(): void {
    this.isLoading.set(true);
    this.adminService.listAlmuerzos().subscribe({
      next: (data) => {
        this.almuerzos.set(data);
        this.isLoading.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar los almuerzos.');
        this.isLoading.set(false);
      },
    });
  }

  editarAlmuerzo(a: TipoAlmuerzo): void {
    this.modoFormulario = 'editar';
    this.almuerzoSeleccionado = a;
    this.form = { nombre: a.nombre, descripcion: a.descripcion, precio: a.precio };
    this.limpiarMensajes();
  }

  cancelar(): void {
    this.modoFormulario = 'crear';
    this.almuerzoSeleccionado = null;
    this.form = { nombre: '', descripcion: '', precio: 0 };
    this.limpiarMensajes();
  }

  guardar(): void {
    if (!this.form.nombre.trim()) {
      this.error.set('El nombre es obligatorio.');
      return;
    }
    this.isSaving.set(true);
    this.limpiarMensajes();

    const obs$ = this.modoFormulario === 'crear'
      ? this.adminService.crearAlmuerzo(this.form)
      : this.adminService.actualizarAlmuerzo(this.almuerzoSeleccionado!.id, this.form);

    obs$.subscribe({
      next: (res) => {
        this.exito.set(res.mensaje);
        this.isSaving.set(false);
        this.cancelar();
        this.cargarAlmuerzos();
      },
      error: () => {
        this.error.set('Ocurrió un error al guardar.');
        this.isSaving.set(false);
      },
    });
  }

  eliminar(id: number): void {
    if (!confirm('¿Estás seguro de que quieres eliminar este almuerzo?')) return;
    this.adminService.eliminarAlmuerzo(id).subscribe({
      next: (res) => {
        this.exito.set(res.mensaje);
        this.cargarAlmuerzos();
      },
      error: () => {
        this.error.set('No se pudo eliminar el almuerzo.');
      },
    });
  }

  private limpiarMensajes(): void {
    this.error.set('');
    this.exito.set('');
  }
}