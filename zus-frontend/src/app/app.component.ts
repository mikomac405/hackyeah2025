import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: false
})
export class AppComponent implements OnInit {
  title = 'Symulator Emerytalny ZUS';
  currentRoute = '';

  constructor(private router: Router) {}

  ngOnInit() {
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe((event) => {
        this.currentRoute = (event as NavigationEnd).url;
      });
  }

  navigateHome() {
    this.router.navigate(['/home']);
  }

  navigateToSimulation() {
    this.router.navigate(['/simulation']);
  }

  navigateToResults() {
    this.router.navigate(['/results']);
  }

  navigateToDashboard() {
    this.router.navigate(['/dashboard']);
  }
}