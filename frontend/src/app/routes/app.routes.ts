import { Routes } from '@angular/router';
import { Home } from '../components/home/home';
import { Login } from '../components/login/login';
import { Registrar } from '../components/registrar/registrar';
import { AuthGuard } from '../guards/auth.guard';
import { RoleGuard } from '../guards/role.guard';

export const routes: Routes = [
  {
    path: 'logni',
    component: Login,
    title: 'login',
  },
  {
    path: 'registrar',
    component: Registrar,
    title: 'Register',
  },
  {
    path: '',
    component: Home,
    title: 'home',
  },
  {
    path: 'admin',
    loadChildren: () => import('../admin/admin.routes').then((m) => m.routes),
    canActivate: [AuthGuard, RoleGuard],
    data: { role: 'admin' },
    title: 'admin',
  },
  {
    path: '**', 
    redirectTo: '' 
  }
];
