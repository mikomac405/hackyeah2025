import { Component, OnInit } from '@angular/core';
import { DataService } from '../../core/services/data.service';
import { PensionCalculatorService } from '../../core/services/pension-calculator.service';
import { HistoricalData, RegionalStats, PensionGroup } from '../../core/models/pension-data.model';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  standalone: false
})
export class DashboardComponent implements OnInit {
  historicalData: HistoricalData | null = null;
  regionalStats: RegionalStats | null = null;
  pensionGroups: PensionGroup[] = [];
  isLoading = true;

  constructor(
    private dataService: DataService,
    private pensionCalculator: PensionCalculatorService
  ) {}

  ngOnInit() {
    this.loadDashboardData();
  }

  loadDashboardData() {
    this.dataService.getHistoricalData().subscribe(
      data => this.historicalData = data
    );

    this.dataService.getRegionalStats().subscribe(
      stats => this.regionalStats = stats
    );

    this.pensionCalculator.getPensionGroups().subscribe(
      groups => {
        this.pensionGroups = groups;
        this.isLoading = false;
      }
    );
  }
}
