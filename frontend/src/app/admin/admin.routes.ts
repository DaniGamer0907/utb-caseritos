import { Routes } from '@angular/router';
import { Login } from '../login/login';
import { Admin } from './admin';
import { Registrar } from '../registrar/registrar';

export const routes: Routes = [
    {
        path: '',
        component: Admin,
        title: 'AdminDashboard'
    },    
];
