import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CartStore } from '../../../services/cart/cart-store';

@Component({
  selector: 'app-cart-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cart-panel.component.html',
  styleUrl: './cart-panel.component.css',
})
export class CartPanelComponent {
  store = inject(CartStore);

  sendWhatsApp() {
    const msg = this.store.buildWhatsAppMessage();
    const url = `https://wa.me/573016221347?text=${encodeURIComponent(msg)}`;
    window.open(url, '_blank', 'noopener');
  }
}
