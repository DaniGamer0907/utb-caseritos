import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CartStore } from '../../../services/cart/cart-store';
import { CheckoutComponent } from '../checkout/checkout.component';

@Component({
  selector: 'app-cart-panel',
  standalone: true,
  imports: [CommonModule, CheckoutComponent],
  templateUrl: './cart-panel.component.html',
  styleUrl: './cart-panel.component.css',
})
export class CartPanelComponent {
  store = inject(CartStore);

  goToCheckout() {
    this.store.showCartPanel.set(false);
    this.store.showCheckout.set(true);
  }
}
