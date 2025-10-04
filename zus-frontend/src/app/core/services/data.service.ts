import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { delay } from 'rxjs/operators';
import { UsageLogData, RegionalStats, HistoricalData } from '../models/pension-data.model';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private apiUrl = '/api'; // W produkcji to będzie rzeczywisty URL API

  constructor(private http: HttpClient) { }

  /**
   * Pobiera dane historyczne (w przyszłości z API)
   */
  getHistoricalData(): Observable<HistoricalData> {
    const mockData: HistoricalData = {
      years: [2020, 2021, 2022, 2023, 2024],
      averageSalaries: [4500, 4650, 4800, 4950, 5100],
      inflationRates: [2.8, 3.2, 2.5, 3.1, 2.9],
      pensionFundGrowth: [1.5, 2.1, 1.8, 2.3, 1.9]
    };

    return of(mockData).pipe(delay(500));
  }

  /**
   * Loguje użycie aplikacji
   */
  logUsage(data: UsageLogData): Observable<{success: boolean}> {
    console.log('Logging usage data:', data);
    
    // W przyszłości będzie prawdziwy API call:
    // return this.http.post<{success: boolean}>(`${this.apiUrl}/usage-log`, data);
    
    return of({ success: true }).pipe(delay(200));
  }

  /**
   * Pobiera statystyki regionalne
   */
  getRegionalStats(postalCode?: string): Observable<RegionalStats> {
    const mockStats: RegionalStats = {
      region: postalCode ? `Region ${postalCode.substring(0, 2)}` : 'Cała Polska',
      averagePension: 2800 + (Math.random() * 400 - 200), // ±200 zł różnicy
      participantsCount: Math.floor(Math.random() * 1000) + 500,
      medianAge: Math.floor(Math.random() * 10) + 45
    };

    return of(mockStats).pipe(delay(300));
  }

  /**
   * Eksportuje dane do Excel (dla administratora)
   */
  exportToExcel(data: UsageLogData[]): Observable<Blob> {
    // Symulacja generowania Excel'a
    const csvContent = this.convertToCSV(data);
    const blob = new Blob([csvContent], { type: 'text/csv' });
    
    return of(blob).pipe(delay(1000));
  }

  private convertToCSV(data: UsageLogData[]): string {
    const headers = [
      'Data',
      'Godzina',
      'Oczekiwana emerytura',
      'Wiek',
      'Płeć',
      'Wynagrodzenie',
      'Uwzględniono chorobowe',
      'Zgromadzone środki',
      'Emerytura rzeczywista',
      'Emerytura urealniona',
      'Kod pocztowy'
    ];

    const rows = data.map(item => [
      item.timestamp.toLocaleDateString('pl-PL'),
      item.timestamp.toLocaleTimeString('pl-PL'),
      item.expectedPension || '',
      item.age,
      item.gender === 'female' ? 'Kobieta' : 'Mężczyzna',
      item.grossSalary,
      item.sickLeaveIncluded ? 'Tak' : 'Nie',
      item.currentFunds || '',
      item.realPension,
      item.inflationAdjustedPension,
      item.postalCode || ''
    ]);

    return [headers, ...rows]
      .map(row => row.map(field => `"${field}"`).join(','))
      .join('\n');
  }
}