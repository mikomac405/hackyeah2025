import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { timeout } from 'rxjs/operators';
import { UsageLogData, RegionalStats, HistoricalData } from '../models/pension-data.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getHistoricalData(): Observable<HistoricalData> {
    return this.http.get<HistoricalData>(`${this.apiUrl}/historical-data`)
      .pipe(
        timeout(10000)
      );
  }

  logUsage(data: UsageLogData): Observable<{success: boolean}> {
    console.log('📊 Logowanie użycia do backend:', data);
    
    const payload = {
      timestamp: data.timestamp.toISOString(),
      expected_pension: data.expectedPension,
      age: data.age,
      gender: data.gender,
      gross_salary: data.grossSalary,
      sick_leave_included: data.sickLeaveIncluded,
      current_funds: data.currentFunds,
      real_pension: data.realPension,
      inflation_adjusted_pension: data.inflationAdjustedPension,
      postal_code: data.postalCode
    };

    return this.http.post<{success: boolean}>(`${this.apiUrl}/log-usage`, payload)
      .pipe(
        timeout(5000)
      );
  }

  getRegionalStats(postalCode?: string): Observable<RegionalStats> {
    const params = postalCode ? `?postal_code=${postalCode}` : '';
    
    return this.http.get<RegionalStats>(`${this.apiUrl}/regional-stats${params}`)
      .pipe(
        timeout(5000)
      );
  }


  exportToExcel(): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/export-excel`, { 
      responseType: 'blob',
      headers: {
        'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      }
    }).pipe(
      timeout(30000) // 30 sekund na export
    );
  }

  checkBackendHealth(): Observable<{status: string, version: string}> {
    return this.http.get<{status: string, version: string}>(`${this.apiUrl}/health`)
      .pipe(
        timeout(3000)
      );
  }

  getAllSessions(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/admin/sessions`)
      .pipe(
        timeout(10000)
      );
  }

  getUsageStatistics(dateFrom?: string, dateTo?: string): Observable<any> {
    let params = '';
    if (dateFrom && dateTo) {
      params = `?date_from=${dateFrom}&date_to=${dateTo}`;
    }
    
    return this.http.get(`${this.apiUrl}/admin/statistics${params}`)
      .pipe(
        timeout(10000)
      );
  }
}