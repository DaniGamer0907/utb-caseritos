import { Component, Input, inject, signal, OnInit } from '@angular/core';
import { CommonModule,} from '@angular/common';
import { Store } from '../../../services/status/store';
import { CartStore } from '../../../services/cart/cart-store';
import { HomeMenuItem } from '../../../services/home/home.service';

@Component({
  selector: 'app-menu-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './menu-card.component.html',
  styleUrl: './menu-card.component.css'
})
export class MenuCardComponent implements OnInit {
  store = inject(Store);
  cartStore = inject(CartStore);

  @Input({ required: true }) item!: HomeMenuItem;

  selectedProtein = signal<{ id: number; nombre: string } | null>(null);
  isAdded = signal(false);

  ngOnInit(): void {
    if (this.item.proteins.length > 0) {
      this.selectedProtein.set(this.item.proteins[0]);
    }
  }

  setProtein(protein: { id: number; nombre: string }): void {
    this.selectedProtein.set(protein);
  }

  handleAddToCart(): void {
    const protein = this.selectedProtein();
    if (!protein) return;

    if (!this.cartStore.isAuthenticated()) {
      // Si no está autenticado, abre el modal de login
      this.cartStore.openLogin();
      return;
    }
    this.cartStore.addToCart(this.item, protein);
    this.isAdded.set(true);
    // Abre el panel del carrito para que vea que se agregó
    this.cartStore.showCartPanel.set(true);
    setTimeout(() => this.isAdded.set(false), 1500);
  }
}
