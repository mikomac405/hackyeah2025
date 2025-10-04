import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-loading-spinner',
  templateUrl: './loading-spinner.component.html',
  styleUrls: ['./loading-spinner.component.css'],
  standalone: false
})
export class LoadingSpinnerComponent {
  @Input() message = 'Ładowanie...';
  @Input() diameter = 40;
  @Input() ariaLabel = 'Trwa ładowanie danych';
}
