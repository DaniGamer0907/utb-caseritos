import { Component,inject,signal } from '@angular/core';
import { Store } from '../services/status/store';
@Component({
  selector: 'app-home',
  imports: [],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {
  store = inject(Store)
  readonly brand = 'Caseritos';
    readonly selectedProteins = signal<Record<string, string>>(
    this.store.menuItems.reduce(
      (acc, item) => ({ ...acc, [item.id]: item.proteins[0] }),
      {} as Record<string, string>
    )
  );

    scrollToMenu(): void {
    document.getElementById('menu')?.scrollIntoView({ behavior: 'smooth' });
  }

    setProtein(menuItemId: string, protein: string): void {
    this.selectedProteins.update((current) => ({ ...current, [menuItemId]: protein }));
  }
  
}
