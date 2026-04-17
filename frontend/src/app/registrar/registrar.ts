import { Component, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthService } from '../auth-service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-registrar',
  imports: [RouterModule,FormsModule],
  templateUrl: 'registrar.html',
  styleUrls: ['./registrar.css'],
})
export class Registrar {
  usuario = {
    name: '',
    lastname: '',
    password: '',
    address: '',
    phone: '',
    email: ''
  };
  authService: AuthService = inject(AuthService);
  onRegistro(){
    console.log("hola1")
    this.authService.registro(this.usuario).subscribe({
      next: (res: any) => {
        alert(res.message); // "Usuario registrado correctamente"
        // Aquí podrías redirigir al login
      },
      error: (err) => {
        alert('Error: ' + err.error.detail);
      }
    });
    console.log("hola2")
  }
}
