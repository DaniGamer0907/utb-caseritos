import { Injectable,computed,signal } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class Store {
    readonly brand = 'Caseritos';
    readonly whatsappNumber = '573016221347';
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

     readonly menuItems = [
    {
      id: 'seco',
      name: 'Almuerzo Seco',
      description:
        'Arroz + lentejas + ensalada + patacon + jugo. Incluye proteina a eleccion.',
      price: 13000,
      image:
        'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-eMu5FvGyMG2rfjj8KO2AfRXCw0tzTo.png',
      proteins: ['Cerdo asado', 'Pechuga bechamel', 'Cerdo BBQ']
    },
    {
      id: 'corriente',
      name: 'Almuerzo Corriente',
      description:
        'Arroz + lentejas + ensalada + patacon + sopa del dia + jugo. El almuerzo mas completo.',
      price: 16000,
      image:
        'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-eMu5FvGyMG2rfjj8KO2AfRXCw0tzTo.png',
      proteins: ['Cerdo asado', 'Pechuga bechamel', 'Cerdo BBQ']
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
