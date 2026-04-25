import { Routes } from '@angular/router';
import { Home } from './home/home';
import { Login } from './login/login';
import { Registrar } from './registrar/registrar';
import { AuthGuard } from './guards/auth.guard';
import { RoleGuard } from './guards/role.guard';

export const routes: Routes = [
  {
    path: '',
    component: Login,
    title: 'login',
  },
  {
    path: 'Registrar',
    component: Registrar,
    title: 'Register',
  },
  {
    path: 'home',
    component: Home,
    canActivate: [AuthGuard],
    title: 'home',
  },
  {
    path: 'admin',
    loadChildren: () => import('./admin/admin.routes').then((m) => m.routes),
    canActivate: [AuthGuard, RoleGuard],
    data: { role: 'admin' },
    title: 'admin',
  },
  {
    path: '**', 
    redirectTo: '' 
  }
];
