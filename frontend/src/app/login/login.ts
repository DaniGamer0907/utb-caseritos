import { Component, inject } from '@angular/core';
import { RouterModule, Router } from '@angular/router';
import { AuthService } from '../auth-service';
import { FormsModule } from '@angular/forms';
import { Autenticacion } from '../services/auth/autenticacion';
@Component({
  selector: 'app-login',
  imports: [RouterModule, FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  //constructor(private router: Router){}

  authService: AuthService = inject(AuthService);
  router: Router = inject(Router);
  email = '';
  password = '';
  onLogin(){
    this.authService.login(this.email, this.password).subscribe({
      next: (res: any) => {
        localStorage.setItem('token', res.access_token);
        localStorage.setItem('role', res.role);
        console.log('¡Adentro!', res.role);
        this.router.navigate(['/admin'])
      },
      error: (err) => alert('Error: ' + err.error.detail)
    });
  }
}
