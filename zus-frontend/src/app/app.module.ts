import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

// Angular Material Modules
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatSliderModule } from '@angular/material/slider';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { MatStepperModule } from '@angular/material/stepper';
import { MatTabsModule } from '@angular/material/tabs';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDialogModule } from '@angular/material/dialog';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

// Core module
import { CoreModule } from './core/core.module';

// Feature components
import { HomeComponent } from './features/home/home.component';
import { SimulationFormComponent } from './features/simulation/simulation-form.component';
import { ResultsComponent } from './features/results/results.component';
import { DashboardComponent } from './features/dashboard/dashboard.component';

// Shared components
import { LoadingSpinnerComponent } from './shared/components/loading-spinner/loading-spinner.component';
import { ChartComponent } from './shared/components/chart/chart.component';
import { BackendStatusComponent } from './shared/components/backend-status/backend-status.component';

// Shared pipes
import { CurrencyPlnPipe } from './shared/pipes/currency-pln.pipe';
import { PercentagePipe } from './shared/pipes/percentage.pipe';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    SimulationFormComponent,
    ResultsComponent,
    DashboardComponent,
    LoadingSpinnerComponent,
    ChartComponent,
    CurrencyPlnPipe,
    PercentagePipe,
    BackendStatusComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    FormsModule,
    HttpClientModule,
    
    // Core Module
    CoreModule,
    
    // Angular Material
    MatToolbarModule,
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatSliderModule,
    MatCheckboxModule,
    MatProgressSpinnerModule,
    MatIconModule,
    MatStepperModule,
    MatTabsModule,
    MatSnackBarModule,
    MatDialogModule,
    
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }