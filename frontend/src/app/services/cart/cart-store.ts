import { Injectable, signal, computed, effect, inject } from '@angular/core';
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
    this.cart().reduce((sum, item) => sum + item.quantity, 0)
  );

  readonly cartTotal = computed(() =>
    this.cart().reduce((sum, item) => sum + item.menuItem.price * item.quantity, 0)
  );

  constructor() {
    effect(() => {
      const currentUser = this.authService.getUser();
      this.isAuthenticated.set(!!currentUser);
      this.user.set(currentUser);
    });
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
        next: (res: { role: string }) => {
          resolve(true);
          if (res.role === 'admin') {
            this.router.navigate(['/admin']);
          }
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
    this.authService.logout();
    this.cart.set([]);
    this.router.navigate(['/']);
  }

  // ── Cart ──────────────────────────────────────────
  addToCart(menuItem: HomeMenuItem, selectedProtein: { id: number; nombre: string }) {
    const existing = this.cart().find(
      (item) => item.menuItem.id === menuItem.id && item.selectedProtein.id === selectedProtein.id
    );

    if (existing) {
      this.updateQuantity(existing.id, existing.quantity + 1);
      return;
    }

    this.cart.update((items) => [
      ...items,
      { id: `${menuItem.id}-${selectedProtein.id}-${Date.now()}`, menuItem, selectedProtein, quantity: 1 },
    ]);
  }

  updateQuantity(itemId: string, qty: number) {
    if (qty <= 0) {
      this.removeFromCart(itemId);
      return;
    }

    this.cart.update((items) =>
      items.map((item) => item.id === itemId ? { ...item, quantity: qty } : item)
    );
  }

  removeFromCart(itemId: string) {
    this.cart.update((items) => items.filter((item) => item.id !== itemId));
  }

  clearCart() {
    this.cart.set([]);
  }

  toggleCartPanel() {
    this.showCartPanel.update((value) => !value);
  }

  formatPrice(value: number): string {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0,
    }).format(value);
  }

  buildWhatsAppMessage(): string {
    const lines = this.cart()
      .map((item) => `• ${item.quantity}x ${item.menuItem.name} (${item.selectedProtein.nombre}) — ${this.formatPrice(item.menuItem.price * item.quantity)}`)
      .join('\n');

    return `Hola! Quiero hacer un pedido:\n\n${lines}\n\nTotal: ${this.formatPrice(this.cartTotal())}`;
  }
}
