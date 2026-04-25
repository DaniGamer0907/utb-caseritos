import { Component, inject } from '@angular/core';
import { RouterModule, Router } from '@angular/router';
import { AuthService } from '../auth-service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  imports: [RouterModule, FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  authService: AuthService = inject(AuthService);
  router: Router = inject(Router);
  email = '';
  password = '';

  onLogin() {
    this.authService.login(this.email, this.password).subscribe({
      next: (res: any) => {
        const role = this.authService.getRol() ?? res.role;

        if (role === 'admin') {
          this.router.navigate(['/admin']);
        } else {
          this.router.navigate(['/home']);
        }
      },
      error: (err) => alert('Error: ' + err.error.detail),
    });
  }
}
