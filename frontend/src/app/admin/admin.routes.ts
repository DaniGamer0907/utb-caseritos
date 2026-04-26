import { Routes } from '@angular/router';
import { Login } from '../components/login/login';
import { Admin } from './admin';
import { Registrar } from '../components/registrar/registrar';

export const routes: Routes = [
    {
        path: '',
        component: Admin,
        title: 'AdminDashboard'
    },    
];
