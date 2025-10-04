import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HomeComponent } from './features/home/home.component';
import { SimulationFormComponent } from './features/simulation/simulation-form.component';
import { ResultsComponent } from './features/results/results.component';
import { DashboardComponent } from './features/dashboard/dashboard.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    component: HomeComponent,
    title: 'Strona główna - Symulator Emerytalny ZUS'
  },
  {
    path: 'simulation',
    component: SimulationFormComponent,
    title: 'Symulacja emerytury - ZUS'
  },
  {
    path: 'results',
    component: ResultsComponent,
    title: 'Wyniki symulacji - ZUS'
  },
  {
    path: 'dashboard',
    component: DashboardComponent,
    title: 'Dashboard zaawansowany - ZUS'
  },
  {
    path: '**',
    redirectTo: '/home'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    enableTracing: false,
    scrollPositionRestoration: 'top'
  })],
  exports: [RouterModule]
})
export class AppRoutingModule { }