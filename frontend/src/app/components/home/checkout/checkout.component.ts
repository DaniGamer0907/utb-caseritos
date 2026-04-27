import { Component, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CartStore } from '../../../services/cart/cart-store';

type PaymentMethod = 'efectivo' | 'nequi' | 'whatsapp' | null;

@Component({
  selector: 'app-checkout',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './checkout.component.html',
  styleUrl: './checkout.component.css',
})
export class CheckoutComponent {
  store = inject(CartStore);

  screen = signal<'checkout' | 'confirmed'>('checkout');
  paymentMethod = signal<PaymentMethod>(null);

  // ── Efectivo ──────────────────────────────────────
  bills = [100000, 50000, 20000, 10000, 5000, 2000];
  selectedBills = signal<number[]>([]);
  addCoins = signal(false);
  coinsAmount = signal(0);

  billsTotal = computed(() =>
    this.selectedBills().reduce((sum, b) => sum + b, 0)
  );

  totalEntregado = computed(() =>
    this.billsTotal() + (this.addCoins() ? (this.coinsAmount() || 0) : 0)
  );

  vuelto = computed(() =>
    Math.max(0, this.totalEntregado() - this.store.cartTotal())
  );

  faltante = computed(() =>
    Math.max(0, this.store.cartTotal() - this.totalEntregado())
  );

  // ── Nequi ─────────────────────────────────────────
  readonly nequiNumber = '300 123 4567';
  nequiRef = signal('');
  nequiCopied = signal(false);

  // ── Pedido ────────────────────────────────────────
  orderNumber = signal('');
  confirming = signal(false);

  // ── Helpers ───────────────────────────────────────
  selectMethod(m: PaymentMethod) {
    this.paymentMethod.set(m);
    this.selectedBills.set([]);
    this.addCoins.set(false);
    this.coinsAmount.set(0);
    this.nequiRef.set('');
  }

  toggleBill(bill: number) {
    const cur = this.selectedBills();
    this.selectedBills.set(
      cur.includes(bill) ? cur.filter(b => b !== bill) : [...cur, bill]
    );
  }

  isBillSelected = (bill: number) => this.selectedBills().includes(bill);

  copyNequi() {
    navigator.clipboard.writeText(this.nequiNumber.replace(/\s/g, ''));
    this.nequiCopied.set(true);
    setTimeout(() => this.nequiCopied.set(false), 2200);
  }

  canConfirm = computed(() => {
    const m = this.paymentMethod();
    if (!m) return false;
    if (m === 'efectivo') return true; // siempre puede confirmar (billetes son info para domiciliario)
    if (m === 'nequi') return this.nequiRef().trim().length >= 4;
    return true; // whatsapp
  });

  get paymentLabel() {
    const m = this.paymentMethod();
    if (m === 'nequi') return 'Nequi';
    if (m === 'whatsapp') return 'Coordinado por WhatsApp';
    if (this.selectedBills().length > 0) {
      return `Efectivo — vuelto de ${this.store.formatPrice(this.vuelto())}`;
    }
    return 'Efectivo al recibir';
  }

  get cashSummaryForAdmin(): string {
    if (this.paymentMethod() !== 'efectivo') return '';
    const bills = this.selectedBills();
    if (!bills.length) return 'Efectivo exacto';
    const billsStr = bills.map(b => `$${(b/1000).toFixed(0)}k`).join(' + ');
    return `Billetes: ${billsStr} = ${this.store.formatPrice(this.totalEntregado())} → Vuelto: ${this.store.formatPrice(this.vuelto())}`;
  }

  async confirm() {
    if (!this.canConfirm()) return;

    if (this.paymentMethod() === 'whatsapp') {
      this.sendWhatsApp();
      return;
    }

    this.confirming.set(true);
    await new Promise(r => setTimeout(r, 1200));
    this.orderNumber.set('A' + Math.floor(1000 + Math.random() * 9000));
    this.confirming.set(false);
    this.screen.set('confirmed');
  }

  sendWhatsApp() {
    const items = this.store.cart()
      .map(i => `• ${i.quantity}x ${i.menuItem.name} (${i.selectedProtein}) — ${this.store.formatPrice(i.menuItem.price * i.quantity)}`)
      .join('\n');
    const cashNote = this.cashSummaryForAdmin ? `\n💵 Pago: ${this.cashSummaryForAdmin}` : '';
    const msg = `Hola Caseritos! 🍽️ Quiero hacer un pedido:\n\n${items}\n\nTotal: ${this.store.formatPrice(this.store.cartTotal())}${cashNote}\n\nMétodo de pago: ${this.paymentLabel}`;
    window.open(`https://wa.me/573016221347?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
    // Mostrar confirmación igual
    this.orderNumber.set('A' + Math.floor(1000 + Math.random() * 9000));
    this.screen.set('confirmed');
  }

  goHome() {
    this.store.clearCart();
    this.store.showCheckout.set(false);
    this.screen.set('checkout');
    this.paymentMethod.set(null);
  }

  editOrder() {
    this.store.showCheckout.set(false);
    this.store.showCartPanel.set(true);
  }

  get firstItem() { return this.store.cart()[0] ?? null; }
}
