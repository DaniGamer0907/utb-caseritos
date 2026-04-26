import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { CartStore } from '../../../services/cart/cart-store';
import { CartPanelComponent } from '../cart-panel/cart-panel.component';
import { AuthModalComponent } from './auth-modal/auth-modal.component';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule, CartPanelComponent, AuthModalComponent],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
})
export class NavbarComponent {
  store = inject(CartStore);
  mobileMenuOpen = signal(false);

  toggleMobile() {
    this.mobileMenuOpen.update(v => !v);
  }

  scrollToMenu() {
    document.getElementById('menu')?.scrollIntoView({ behavior: 'smooth' });
    this.mobileMenuOpen.set(false);
  }

  handleLogin() {
    this.store.openLogin();
    this.mobileMenuOpen.set(false);
  }

  handleRegister() {
    this.store.openRegister();
    this.mobileMenuOpen.set(false);
  }

  handleLogout() {
    this.store.logout();
    this.mobileMenuOpen.set(false);
  }
}
