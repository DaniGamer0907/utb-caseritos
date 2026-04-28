import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService, Proteina, ProteinaPayload } from '../../../services/admin/admin.service';

@Component({
  selector: 'app-proteina',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './proteina.html',
})
export class ProteinaComponent implements OnInit {
  private readonly adminService = inject(AdminService);

  proteinas = signal<Proteina[]>([]);
  isLoading  = signal(true);
  isSaving   = signal(false);
  error      = signal('');
  exito      = signal('');

  modoFormulario: 'crear' | 'editar' = 'crear';
  proteinaSeleccionada: Proteina | null = null;
  form: ProteinaPayload = { nombre: '', avaliable: 1 };

  ngOnInit(): void {
    this.cargarProteinas();
  }

  private cargarProteinas(): void {
    this.isLoading.set(true);
    this.adminService.listProteinas().subscribe({
      next: (data) => {
        this.proteinas.set(data);
        this.isLoading.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar las proteínas.');
        this.isLoading.set(false);
      },
    });
  }

  editarProteina(p: Proteina): void {
    this.modoFormulario = 'editar';
    this.proteinaSeleccionada = p;
    this.form = { nombre: p.nombre, avaliable: p.avaliable };
    this.limpiarMensajes();
  }

  cancelar(): void {
    this.modoFormulario = 'crear';
    this.proteinaSeleccionada = null;
    this.form = { nombre: '', avaliable: 1 };
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
      ? this.adminService.crearProteina(this.form)
      : this.adminService.actualizarProteina(this.proteinaSeleccionada!.id, this.form);

    obs$.subscribe({
      next: (res) => {
        this.exito.set(res.mensaje);
        this.isSaving.set(false);
        this.cancelar();
        this.cargarProteinas();
      },
      error: () => {
        this.error.set('Ocurrió un error al guardar. Verifica que tengas sesión de administrador.');
        this.isSaving.set(false);
      },
    });
  }

  eliminar(id: number): void {
    if (!confirm('¿Estás seguro de que quieres eliminar esta proteína?')) return;
    this.adminService.eliminarProteina(id).subscribe({
      next: (res) => {
        this.exito.set(res.mensaje);
        this.cargarProteinas();
      },
      error: () => {
        this.error.set('No se pudo eliminar la proteína.');
      },
    });
  }

  private limpiarMensajes(): void {
    this.error.set('');
    this.exito.set('');
  }
}