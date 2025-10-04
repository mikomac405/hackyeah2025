import { Component, OnInit } from '@angular/core';
import { DataService } from '../../../core/services/data.service';
import { interval } from 'rxjs';
import { startWith, switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-backend-status',
  template: `
    <div class="backend-status" [class]="statusClass">
      <mat-icon>{{ statusIcon }}</mat-icon>
      <span>{{ statusText }}</span>
    </div>
  `,
  styles: [`
    .backend-status {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 16px;
      font-size: 12px;
      font-weight: 500;
    }
    
    .online {
      background-color: #e8f5e8;
      color: #2e7d32;
    }
    
    .offline {
      background-color: #ffebee;
      color: #c62828;
    }
    
    .checking {
      background-color: #fff3e0;
      color: #ef6c00;
    }
  `],
  standalone: false
})
export class BackendStatusComponent implements OnInit {
  statusClass = 'checking';
  statusIcon = 'hourglass_empty';
  statusText = 'Sprawdzam backend...';

  constructor(private dataService: DataService) {}

  ngOnInit() {
    // Sprawdzaj status co 30 sekund
    interval(30000)
      .pipe(
        startWith(0),
        switchMap(() => this.dataService.checkBackendHealth())
      )
      .subscribe({
        next: (health) => {
          this.statusClass = 'online';
          this.statusIcon = 'check_circle';
          this.statusText = `Backend online (${health.version})`;
        },
        error: (error) => {
          console.error('❌ Backend offline:', error);
          this.statusClass = 'offline';
          this.statusIcon = 'error';
          this.statusText = 'Backend offline - sprawdź czy uruchomiony!';
        }
      });
  }
}