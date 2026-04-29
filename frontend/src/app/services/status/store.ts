import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class Store {
    readonly brand = 'Caseritos';
    readonly whatsappNumber = '573016380266';
    readonly featureCards = [
    {
      icon: 'S',
      title: 'Sabor Casero',
      text: 'Cocinamos con recetas tradicionales y el amor de hogar.'
    },
    {
      icon: 'F',
      title: 'Ingredientes Frescos',
      text: 'Usamos solo ingredientes frescos y de la mejor calidad.'
    },
    {
      icon: 'W',
      title: 'Pedidos Rapidos',
      text: 'Pide facil por WhatsApp y recibe tu almuerzo al instante.'
    }
  ];

      openWhatsApp(baseMessage?: string): void {
    const url = baseMessage
      ? `https://wa.me/${this.whatsappNumber}?text=${encodeURIComponent(baseMessage)}`
      : `https://wa.me/${this.whatsappNumber}`;
    window.open(url, '_blank', 'noopener');
  }

    formatPrice(price: number): string {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(price);
  }
  
}
