import { Component, Input, OnInit, OnDestroy } from '@angular/core';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css'],
  standalone: false
})
export class ChartComponent implements OnInit, OnDestroy {
  @Input() chartData: any;
  @Input() chartType = 'bar';
  @Input() chartOptions: any = {};

  ngOnInit() {
    // Chart implementation will be added later
  }

  ngOnDestroy() {
    // Cleanup if needed
  }
}
