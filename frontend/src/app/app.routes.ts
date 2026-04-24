import { Routes } from '@angular/router';
import { Home } from './home/home';
import { Login } from './login/login';
import { Registrar } from './registrar/registrar';
import { Admin } from './admin/admin';

export const routes: Routes = [

    {
        path: '',
        component: Home,
        title: 'home'
    },

    // {
    //     path: '',
    //     component: Login,
    //     title: 'login'
    // },
    
    // {
    //     path: 'Registrar',
    //     component: Registrar,
    //     title: 'Register'
    // },

    // {
    //     path: 'admin',
    //     loadChildren: () => import ('./admin/admin.routes').then(m => m.routes)
    // }
];
