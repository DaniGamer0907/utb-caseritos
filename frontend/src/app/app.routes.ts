import { Routes } from '@angular/router';
import { Home } from './home/home';
import { Login } from './login/login';
import { Registrar } from './registrar/registrar';

export const routes: Routes = [
    {
        path: 'home',
        component: Home,
        title: 'homePage'
    },
    {
        path: '',
        component: Login,
        title: 'login'
    },

    {
        path: 'Registrar',
        component: Registrar,
        title: 'Register'
    }
];
