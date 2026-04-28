import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { CartStore } from '../../../services/cart/cart-store';
import { CheckoutDetallePayload, CheckoutPagoPayload, PedidosService } from '../../../services/pedidos/pedidos-service';

type PaymentMethod = 'efectivo' | 'nequi' | 'whatsapp' | null;

@Component({
  selector: 'app-checkout',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './checkout.component.html',
  styleUrl: './checkout.component.css',
})
export class CheckoutComponent {
  readonly store = inject(CartStore);
  private readonly pedidosService = inject(PedidosService);

  readonly screen = signal<'checkout' | 'confirmed'>('checkout');
  readonly paymentMethod = signal<PaymentMethod>(null);

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

  readonly orderNumber = signal('');
  readonly confirming = signal(false);
  readonly submitError = signal('');

  readonly canConfirm = computed(() => {
    const method = this.paymentMethod();
    if (!method || this.store.cart().length === 0) {
      return false;
    }

    if (method === 'efectivo') {
      return true;
    }

    if (method === 'nequi') {
      return this.nequiRef().trim().length >= 4;
    }

    return true;
  });

  selectMethod(method: PaymentMethod) {
    this.paymentMethod.set(method);
    this.submitError.set('');
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

  get paymentLabel(): string {
    const method = this.paymentMethod();

    if (method === 'nequi') {
      return 'Nequi';
    }

    if (method === 'whatsapp') {
      return 'Coordinado por WhatsApp';
    }

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

    this.submitError.set('');
    this.confirming.set(true);

    try {
      const pagoPayload: CheckoutPagoPayload = {
        metodopago: this.paymentMethod() || 'efectivo',
        diadelpago: new Date().toISOString().split('T')[0], // YYYY-MM-DD
        referencia: this.paymentMethod() === 'nequi' ? this.nequiRef().trim() : undefined
      };

      const detallesPayload: CheckoutDetallePayload[] = this.store.cart().map((item) => ({
        proteinaid: item.selectedProtein.id,
        tipalmuerzoid: item.menuItem.apiId,
        cantidad: item.quantity,
      }));

      await firstValueFrom(
        this.pedidosService.crearPedido({
          sugerencia: this.buildOrderSuggestion(),
          pago: pagoPayload,
          detalles: detallesPayload,
        })
      );

      this.orderNumber.set(`A${Date.now().toString().slice(-6)}`);
      this.screen.set('confirmed');
    } catch (err) {
      console.error('Error al confirmar pedido:', err);
      this.submitError.set(
        'No fue posible enviar el pedido a la API. Verifica tu sesión e inténtalo de nuevo.'
      );
    } finally {
      this.confirming.set(false);
    }
  }

  sendWhatsApp() {
    const items = this.store.cart()
      .map(i => `• ${i.quantity}x ${i.menuItem.name} (${i.selectedProtein.nombre}) — ${this.store.formatPrice(i.menuItem.price * i.quantity)}`)
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
    this.submitError.set('');
  }

  editOrder() {
    this.store.showCheckout.set(false);
    this.store.showCartPanel.set(true);
  }

  get firstItem() {
    return this.store.cart()[0] ?? null;
  }

  private buildOrderSuggestion(): string {
    const items = this.store.cart()
      .map((item) => `${item.quantity}x ${item.menuItem.name} (${item.selectedProtein.nombre})`)
      .join(', ');

    const extras = [
      `Metodo de pago: ${this.paymentLabel}`,
      this.paymentMethod() === 'efectivo' ? this.cashSummaryForAdmin : '',
      this.paymentMethod() === 'nequi' ? `Referencia Nequi: ${this.nequiRef().trim()}` : '',
      `Total: ${this.store.formatPrice(this.store.cartTotal())}`,
    ].filter(Boolean);

    return `Pedido web: ${items}. ${extras.join('. ')}`;
  }
}
