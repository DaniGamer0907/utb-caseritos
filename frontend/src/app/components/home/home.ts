import { Component, inject, signal } from '@angular/core';
import { Store } from '../../services/status/store';
import { HomeMenuItem, HomeMenuService } from '../../services/home/home.service';
import { MenuCardComponent } from './menu-card/menu-card.component';
import { NavbarComponent } from './navbar/navbar.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [MenuCardComponent, NavbarComponent], 
  templateUrl: './home.html',
  styleUrl: './home.css',
})

export class Home {
  store = inject(Store);
  private readonly homeMenuService = inject(HomeMenuService);
  readonly brand = 'Caseritos';
  readonly menuItems = signal<HomeMenuItem[]>([]);
  readonly isLoading = signal(true);
  readonly errorMessage = signal('');
  readonly selectedProteins = signal<Record<string, string>>({});

  constructor() {
    this.loadMenu();
  }

  private loadMenu(): void {
    this.isLoading.set(true);
    this.errorMessage.set('');

    this.homeMenuService.getMenu().subscribe({
      next: (menuItems) => {
        this.menuItems.set(menuItems);
        this.selectedProteins.set(
          menuItems.reduce(
            (acc, item) => ({
              ...acc,
              [item.id]: item.proteins[0]?.nombre ?? '',
            }),
            {} as Record<string, string>
          )
        );
        this.isLoading.set(false);
      },
      error: (error) => {
        const detail =
          typeof error?.error?.detail === 'string'
            ? error.error.detail
            : 'No fue posible cargar el menu.';
        this.errorMessage.set(detail);
        this.menuItems.set([]);
        this.selectedProteins.set({});
        this.isLoading.set(false);
      },
    });
  }

  scrollToMenu(): void {
    document.getElementById('menu')?.scrollIntoView({ behavior: 'smooth' });
  }

  setProtein(menuItemId: string, protein: string): void {
    this.selectedProteins.update((current) => ({ ...current, [menuItemId]: protein }));
  }
}
