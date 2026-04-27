import { Injectable, signal, computed, inject } from '@angular/core';
import { Router } from '@angular/router';
import { HomeMenuItem } from '../home/home.service';
import { AuthService } from '../auth/auth-service';

export interface CartItem {
  id: string;
  menuItem: HomeMenuItem;
  selectedProtein: { id: number; nombre: string };
  quantity: number;
}

export interface AuthUser {
  name: string;
  email: string;
  role?: string;
}

@Injectable({ providedIn: 'root' })
export class CartStore {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  // ── Auth ──────────────────────────────────────────
  readonly isAuthenticated = signal(false);
  readonly user = signal<AuthUser | null>(null);

  // ── Auth Modal ────────────────────────────────────
  readonly showAuthModal = signal(false);
  readonly authModalType = signal<'login' | 'register'>('login');

  // ── Cart ──────────────────────────────────────────
  readonly cart = signal<CartItem[]>([]);
  readonly showCartPanel = signal(false);
  readonly showCheckout = signal(false);

  readonly cartCount = computed(() =>
    this.cart().reduce((sum, i) => sum + i.quantity, 0)
  );

  readonly cartTotal = computed(() =>
    this.cart().reduce((sum, i) => sum + i.menuItem.price * i.quantity, 0)
  );

  constructor() {
    // Restaurar sesión si ya hay token guardado
    // const token = localStorage.getItem('token');
    // const name = localStorage.getItem('userName');
    // const email = localStorage.getItem('userEmail');
    // if (token && name && email) {
    //   this.isAuthenticated.set(true);
    //   this.user.set({ name, email });
    // }
  }

  // ── Modal ─────────────────────────────────────────
  openLogin() {
    this.authModalType.set('login');
    this.showAuthModal.set(true);
  }

  openRegister() {
    this.authModalType.set('register');
    this.showAuthModal.set(true);
  }

  closeAuthModal() {
    this.showAuthModal.set(false);
  }

  // ── Auth actions (conectados a tu API real) ───────
  login(email: string, password: string): Promise<boolean> {
    return new Promise((resolve) => {
      this.authService.login(email, password).subscribe({
        next: (res: any) => {
          localStorage.setItem('token', res.access_token);
          localStorage.setItem('role', res.role);
          localStorage.setItem('userEmail', email);
          // Usa el nombre del email si no viene en la respuesta
          const name = res.name ?? email.split('@')[0];
          localStorage.setItem('userName', name);
          this.isAuthenticated.set(true);
          this.user.set({ name, email, role: res.role });
          resolve(true);
        },
        error: () => resolve(false),
      });
    });
  }

  register(name: string, lastname: string, email: string, password: string, address: string, phone: string): Promise<boolean> {
    return new Promise((resolve) => {
      const datos = { name, lastname, email, password, address, phone };
      this.authService.registro(datos).subscribe({
        next: () => {
          // Tras registrarse, hace login automático
          this.login(email, password).then(resolve);
        },
        error: () => resolve(false),
      });
    });
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('userName');
    localStorage.removeItem('userEmail');
    this.isAuthenticated.set(false);
    this.user.set(null);
    this.cart.set([]);
    this.router.navigate(['/']);
  }

  // ── Cart ──────────────────────────────────────────
  addToCart(menuItem: HomeMenuItem, selectedProtein: { id: number; nombre: string }) {
    const existing = this.cart().find(
      i => i.menuItem.id === menuItem.id && i.selectedProtein.id === selectedProtein.id
    );
    if (existing) {
      this.updateQuantity(existing.id, existing.quantity + 1);
    } else {
      this.cart.update(items => [
        ...items,
        { id: `${menuItem.id}-${selectedProtein.id}-${Date.now()}`, menuItem, selectedProtein, quantity: 1 },
      ]);
    }
  }

  updateQuantity(itemId: string, qty: number) {
    if (qty <= 0) this.removeFromCart(itemId);
    else this.cart.update(items => items.map(i => i.id === itemId ? { ...i, quantity: qty } : i));
  }

  removeFromCart(itemId: string) {
    this.cart.update(items => items.filter(i => i.id !== itemId));
  }

  clearCart() { this.cart.set([]); }

  toggleCartPanel() { this.showCartPanel.update(v => !v); }

  formatPrice(value: number): string {
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(value);
  }

  buildWhatsAppMessage(): string {
    const lines = this.cart()
      .map(i => `• ${i.quantity}x ${i.menuItem.name} (${i.selectedProtein.nombre}) — ${this.formatPrice(i.menuItem.price * i.quantity)}`)
      .join('\n');
    return `Hola! Quiero hacer un pedido:\n\n${lines}\n\nTotal: ${this.formatPrice(this.cartTotal())}`;
  }
}
