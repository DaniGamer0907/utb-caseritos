import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth/auth-service';

export const RoleGuard: CanActivateFn = (route) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const requiredRole = route.data?.['role'];

  if (!authService.isLoggedIn()) {
    return router.createUrlTree(['/']);
  }

  if (!requiredRole || authService.getRol() === requiredRole) {
    return true;
  }
  
  authService.logout();
  return router.createUrlTree(['/']);
};
