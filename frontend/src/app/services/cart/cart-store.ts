import { Injectable, signal, computed } from '@angular/core';
import { HomeMenuItem } from '../home/home.service';

export interface CartItem {
  id: string;
  menuItem: HomeMenuItem;
  selectedProtein: string;
  quantity: number;
}

export interface AuthUser {
  name: string;
  email: string;
}

@Injectable({ providedIn: 'root' })
export class CartStore {
  // ── Auth ──────────────────────────────────────────
  readonly isAuthenticated = signal(false);
  readonly user = signal<AuthUser | null>(null);

  // ── Auth Modal ────────────────────────────────────
  readonly showAuthModal = signal(false);
  readonly authModalType = signal<'login' | 'register'>('login');

  // ── Cart ──────────────────────────────────────────
  readonly cart = signal<CartItem[]>([]);
  readonly showCartPanel = signal(false);

  readonly cartCount = computed(() =>
    this.cart().reduce((sum, i) => sum + i.quantity, 0)
  );

  readonly cartTotal = computed(() =>
    this.cart().reduce((sum, i) => sum + i.menuItem.price * i.quantity, 0)
  );

  // ── Auth actions ──────────────────────────────────
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

  /** Simula login — conecta con tu AuthService real aquí */
  async login(email: string, password: string): Promise<boolean> {
    // TODO: reemplaza con llamada real a tu API de auth
    await delay(600);
    const name = email.split('@')[0];
    this.user.set({ name, email });
    this.isAuthenticated.set(true);
    return true;
  }

  /** Simula registro */
  async register(name: string, email: string, _password: string): Promise<boolean> {
    await delay(600);
    this.user.set({ name, email });
    this.isAuthenticated.set(true);
    return true;
  }

  logout() {
    this.isAuthenticated.set(false);
    this.user.set(null);
    this.cart.set([]);
  }

  // ── Cart actions ──────────────────────────────────
  addToCart(menuItem: HomeMenuItem, selectedProtein: string) {
    const existing = this.cart().find(
      i => i.menuItem.id === menuItem.id && i.selectedProtein === selectedProtein
    );
    if (existing) {
      this.updateQuantity(existing.id, existing.quantity + 1);
    } else {
      this.cart.update(items => [
        ...items,
        {
          id: `${menuItem.id}-${selectedProtein}-${Date.now()}`,
          menuItem,
          selectedProtein,
          quantity: 1,
        },
      ]);
    }
  }

  updateQuantity(itemId: string, qty: number) {
    if (qty <= 0) {
      this.removeFromCart(itemId);
    } else {
      this.cart.update(items =>
        items.map(i => (i.id === itemId ? { ...i, quantity: qty } : i))
      );
    }
  }

  removeFromCart(itemId: string) {
    this.cart.update(items => items.filter(i => i.id !== itemId));
  }

  clearCart() {
    this.cart.set([]);
  }

  toggleCartPanel() {
    this.showCartPanel.update(v => !v);
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
      .map(i => `• ${i.quantity}x ${i.menuItem.name} (${i.selectedProtein}) — ${this.formatPrice(i.menuItem.price * i.quantity)}`)
      .join('\n');
    return `Hola! Quiero hacer un pedido:\n\n${lines}\n\nTotal: ${this.formatPrice(this.cartTotal())}`;
  }
}

function delay(ms: number) {
  return new Promise(res => setTimeout(res, ms));
}
