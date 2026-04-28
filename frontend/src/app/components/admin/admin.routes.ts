import { Routes } from '@angular/router';
import { Login } from '../login/login';
import { AdminComponent } from './admin';
import { Registrar } from '../registrar/registrar';
import { DashboardComponent } from './dashboard/dashboard';
import { ProteinaComponent } from './proteina/proteina';
import { AlmuerzoComponent } from './almuerzo/almuerzo';
import { PagosComponent } from './pagos/pagos';

export const routes: Routes = [
  {
    path: '',
    component: AdminComponent,
    title: 'AdminDashboard',
    children: [
      { path: '',          redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: DashboardComponent },
      { path: 'proteina',  component: ProteinaComponent },
      { path: 'almuerzo',  component: AlmuerzoComponent },
      { path: 'pagos',     component: PagosComponent },
    ],
  },
];