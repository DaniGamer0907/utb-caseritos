import { Component, Input, inject, signal, OnInit } from '@angular/core';
import { CommonModule, DecimalPipe } from '@angular/common';
import { Store } from '../../services/status/store';
import { HomeMenuItem } from '../../services/home/home.service';

@Component({
  selector: 'app-menu-card',
  standalone: true,
  imports: [CommonModule, DecimalPipe],
  templateUrl: './menu-card.component.html',
  styleUrl: './menu-card.component.css'
})
export class MenuCardComponent implements OnInit {
  store = inject(Store);
  
  @Input({ required: true }) item!: HomeMenuItem;

  // Estado local usando Signals
  selectedProtein = signal<string>('');
  isAdded = signal(false);

  ngOnInit(): void {
    // Inicializamos con la primera proteína disponible
    if (this.item.proteins.length > 0) {
      this.selectedProtein.set(this.item.proteins[0]);
    }
  }

  setProtein(protein: string): void {
    this.selectedProtein.set(protein);
  }

  handleAddToCart(): void {
    // Aquí puedes añadir la lógica de autenticación que mencionaste
    // Por ahora, simulamos el feedback visual de "Agregado"
    this.isAdded.set(true);


    setTimeout(() => this.isAdded.set(false), 1500);
  }
}