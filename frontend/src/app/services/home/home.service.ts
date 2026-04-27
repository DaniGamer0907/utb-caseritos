import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, forkJoin, map } from 'rxjs';

interface TipoAlmuerzoApi {
  id: number;
  nombre: string;
  descripcion: string;
  precio: number;
}

interface ProteinaApi {
  id: number;
  nombre: string;
  avaliable: number;
}

export interface HomeMenuItem {
  id: string;
  apiId: number;
  name: string;
  description: string;
  price: number;
  image: string;
  proteins: { id: number; nombre: string }[];
}

@Injectable({
  providedIn: 'root',
})
export class HomeMenuService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000';
  private readonly defaultImage =
    'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-eMu5FvGyMG2rfjj8KO2AfRXCw0tzTo.png';
  private readonly defaultDescription =
    'Arroz, lentejas, ensalada, patacon y jugo. Elige la proteina disponible del dia.';

  getMenu(): Observable<HomeMenuItem[]> {
    return forkJoin({
      tipos: this.http.get<TipoAlmuerzoApi[]>(`${this.apiUrl}/tipoalmuerzo/listTiposAlmuerzo`),
      proteinas: this.http.get<ProteinaApi[]>(`${this.apiUrl}/proteina/listProteinas`),
    }).pipe(
      map(({ tipos, proteinas }) => {
        const availableProteins = proteinas
          .filter((protein) => Boolean(protein.avaliable))
          .map((protein) => ({ id: protein.id, nombre: protein.nombre }));

        return tipos.map((tipo) => ({
          id: String(tipo.id),
          apiId: tipo.id,
          name: tipo.nombre,
          description: tipo.descripcion,
          price: tipo.precio,
          image: this.defaultImage,
          proteins: availableProteins,
        }));
      })
    );
  }
}
