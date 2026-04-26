import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CartStore } from '../../../../services/cart/cart-store';

@Component({
  selector: 'app-auth-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './auth-modal.component.html',
  styleUrl: './auth-modal.component.css',
})
export class AuthModalComponent {
  store = inject(CartStore);

  name = signal('');
  email = signal('');
  password = signal('');
  confirmPassword = signal('');
  showPassword = signal(false);
  loading = signal(false);
  error = signal('');

  reset() {
    this.name.set(''); this.email.set('');
    this.password.set(''); this.confirmPassword.set('');
    this.error.set(''); this.showPassword.set(false);
  }

  close() {
    this.store.closeAuthModal();
    this.reset();
  }

  switchType() {
    this.store.authModalType.update(t => t === 'login' ? 'register' : 'login');
    this.reset();
  }

  async submit() {
    this.error.set('');
    const email = this.email();
    const password = this.password();

    if (!email || !password) {
      this.error.set('Por favor complete todos los campos'); return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      this.error.set('Por favor ingrese un email válido'); return;
    }
    if (password.length < 6) {
      this.error.set('La contraseña debe tener al menos 6 caracteres'); return;
    }
    if (this.store.authModalType() === 'register') {
      if (!this.name()) { this.error.set('Por favor ingrese su nombre'); return; }
      if (password !== this.confirmPassword()) {
        this.error.set('Las contraseñas no coinciden'); return;
      }
    }

    this.loading.set(true);
    try {
      let ok: boolean;
      if (this.store.authModalType() === 'login') {
        ok = await this.store.login(email, password);
        if (!ok) this.error.set('Email o contraseña incorrectos');
      } else {
        ok = await this.store.register(this.name(), email, password);
        if (!ok) this.error.set('Este email ya está registrado');
      }
      if (ok) this.close();
    } catch {
      this.error.set('Ocurrió un error. Por favor intente de nuevo.');
    } finally {
      this.loading.set(false);
    }
  }
}
