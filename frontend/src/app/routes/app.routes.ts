import { Routes } from '@angular/router';
import { Home } from '../components/home/home';
import { AuthGuard } from '../guards/auth.guard';
import { RoleGuard } from '../guards/role.guard';

export const routes: Routes = [
  {
    path: '',
    component: Home,
    title: 'home',
  },
  {
    path: 'admin',
    loadChildren: () => import('../components/admin/admin.routes').then((m) => m.routes),
    canActivate: [AuthGuard, RoleGuard],
    data: { role: 'admin' },
    title: 'admin',
  },
  {
    path: '**', 
    redirectTo: '' 
  }
];
