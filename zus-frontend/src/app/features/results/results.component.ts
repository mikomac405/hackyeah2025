import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PensionCalculatorService } from '../../core/services/pension-calculator.service';
import { ReportService } from '../../core/services/report.service';
import { PensionCalculationResult, PensionInputData } from '../../core/models/pension-data.model';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css'],
  standalone: false
})
export class ResultsComponent implements OnInit {
  results: PensionCalculationResult | null = null;
  inputData: PensionInputData | null = null;
  isGeneratingReport = false;

  constructor(
    private pensionCalculator: PensionCalculatorService,
    private reportService: ReportService,
    private router: Router
  ) {}

  ngOnInit() {
    this.pensionCalculator.currentCalculation$.subscribe(
      result => this.results = result
    );

    this.pensionCalculator.currentInputData$.subscribe(
      data => this.inputData = data
    );

    // Jeśli brak danych, przekieruj do symulacji
    if (!this.results) {
      this.router.navigate(['/simulation']);
    }
  }

  generateReport() {
    if (this.inputData && this.results) {
      this.isGeneratingReport = true;
      this.reportService.generatePDFReport(this.inputData, this.results).subscribe(
        blob => {
          this.downloadFile(blob, 'raport-emerytury.txt');
          this.isGeneratingReport = false;
        },
        error => {
          console.error('Błąd generowania raportu:', error);
          this.isGeneratingReport = false;
        }
      );
    }
  }

  private downloadFile(blob: Blob, filename: string) {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(url);
  }

  newSimulation() {
    this.pensionCalculator.clearCalculations();
    this.router.navigate(['/simulation']);
  }
}
