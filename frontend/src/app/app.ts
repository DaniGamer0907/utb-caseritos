import { Component, signal } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterModule],
  template: `<router-outlet></router-outlet>`,
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}
