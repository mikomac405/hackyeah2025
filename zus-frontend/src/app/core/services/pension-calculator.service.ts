import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { map, timeout, retry, catchError } from 'rxjs/operators';
import { 
  PensionInputData, 
  PensionCalculationResult, 
  PensionGroup 
} from '../models/pension-data.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PensionCalculatorService {
  private apiUrl = environment.apiUrl;
  
  private currentCalculationSubject = new BehaviorSubject<PensionCalculationResult | null>(null);
  public currentCalculation$ = this.currentCalculationSubject.asObservable();

  private currentInputDataSubject = new BehaviorSubject<PensionInputData | null>(null);
  public currentInputData$ = this.currentInputDataSubject.asObservable();

  private isLoadingSubject = new BehaviorSubject<boolean>(false);
  public isLoading$ = this.isLoadingSubject.asObservable();

  constructor(private http: HttpClient) { }


  calculatePension(inputData: PensionInputData): Observable<PensionCalculationResult> {
    console.log(' Wysyłam dane do Python backend:', inputData);
    
    this.currentInputDataSubject.next(inputData);
    this.isLoadingSubject.next(true);
    
    // Mapujemy dane na format oczekiwany przez backend
    const backendPayload = this.mapToBackendFormat(inputData);
    
    console.log('🔍 DEBUG - Backend payload (co faktycznie wysyłamy):', backendPayload);
    
    return this.http.post<any>(`${this.apiUrl}/calculate-pension`, backendPayload)
      .pipe(
        timeout(environment.apiTimeout),
        retry(2), 
        map(response => {
          console.log('🔍 DEBUG - Raw backend response:', response);
          return this.mapFromBackendFormat(response);
        }),
        map(result => {
          console.log('✅ Otrzymano wyniki z backend (po mapowaniu):', result);
          this.currentCalculationSubject.next(result);
          this.isLoadingSubject.next(false);
          return result;
        })
      );
  }


  getPensionGroups(): Observable<PensionGroup[]> {
    return this.http.get<any[]>(`${this.apiUrl}/pension-groups`)
      .pipe(
        timeout(5000),
        map(response => this.mapPensionGroupsFromBackend(response))
      );
  }


  getRandomFact(): Observable<string> {
    return this.http.get<{fact: string}>(`${this.apiUrl}/random-fact`)
      .pipe(
        timeout(3000),
        map(response => response.fact)
      );
  }

  getRegionalStats(postalCode?: string): Observable<any> {
    const params = postalCode ? `?postal_code=${postalCode}` : '';
    return this.http.get(`${this.apiUrl}/regional-stats${params}`)
      .pipe(
        timeout(5000)
      );
  }


  /**
   * TEST METHOD - sprawdza czy backend w ogóle działa
   */
  testCalculation(): Observable<any> {
    console.log('🧪 Testing backend calculation...');
    return this.http.post<any>(`${this.apiUrl}/test-calculation`, {test: true})
      .pipe(
        timeout(10000),
        map(response => {
          console.log('🧪 Test response:', response);
          return response;
        }),
        catchError((error: any) => {
          console.error('🧪 Test failed:', error);
          throw error;
        })
      );
  }

  checkBackendHealth(): Observable<{status: string, version: string}> {
    return this.http.get<{status: string, version: string}>(`${this.apiUrl}/health`)
      .pipe(
        timeout(3000)
      );
  }


  private mapToBackendFormat(inputData: PensionInputData): any {
    return {
      age: inputData.age,
      gender: inputData.gender,
      grossSalary: inputData.grossSalary,  // Poprawiono: backend oczekuje camelCase
      workStartYear: inputData.workStartYear,  // Poprawiono: backend oczekuje camelCase
      workEndYear: inputData.workEndYear || null,  // Poprawiono: backend oczekuje camelCase
      currentFunds: inputData.currentFunds || 0,  // Poprawiono: backend oczekuje camelCase
      currentSubFunds: inputData.currentSubFunds || 0,  // Poprawiono: backend oczekuje camelCase
      sickLeaveImpact: inputData.sickLeaveImpact || false,  // Poprawiono: backend oczekuje camelCase
      expectedPension: inputData.expectedPension || null,  // Poprawiono: backend oczekuje camelCase
      postalCode: inputData.postalCode || null  // Poprawiono: backend oczekuje camelCase
    };
  }


  private mapFromBackendFormat(response: any): PensionCalculationResult {
    return {
      realAmount: Math.round(response.real_amount || 0),
      inflationAdjustedAmount: Math.round(response.inflation_adjusted_amount || 0),
      replacementRate: Math.round(response.replacement_rate || 0),
      averagePensionComparison: Math.round(response.average_pension_comparison || 0),
      sickLeaveImpact: response.sick_leave_impact ? {
        withSickLeave: Math.round(response.sick_leave_impact.with_sick_leave),
        withoutSickLeave: Math.round(response.sick_leave_impact.without_sick_leave),
        difference: Math.round(response.sick_leave_impact.difference),
        percentageImpact: Math.round(response.sick_leave_impact.percentage_impact)
      } : undefined,
      delayedRetirementScenarios: {
        oneYear: {
          amount: Math.round(response.delayed_retirement_scenarios?.one_year?.amount || 0),
          increase: Math.round(response.delayed_retirement_scenarios?.one_year?.increase || 0)
        },
        twoYears: {
          amount: Math.round(response.delayed_retirement_scenarios?.two_years?.amount || 0),
          increase: Math.round(response.delayed_retirement_scenarios?.two_years?.increase || 0)
        },
        fiveYears: {
          amount: Math.round(response.delayed_retirement_scenarios?.five_years?.amount || 0),
          increase: Math.round(response.delayed_retirement_scenarios?.five_years?.increase || 0)
        }
      },
      requiredWorkExtension: response.required_work_extension || undefined,
      fundsGrowthTimeline: (response.funds_growth_timeline || []).map((item: any) => ({
        year: item.year,
        age: item.age,
        totalFunds: Math.round(item.total_funds),
        annualContribution: Math.round(item.annual_contribution)
      }))
    };
  }

  private mapPensionGroupsFromBackend(response: any[]): PensionGroup[] {
    return response.map(group => ({
      name: group.name,
      description: group.description,
      averageAmount: group.average_amount,
      percentage: group.percentage,
      color: group.color,
      detailedInfo: group.detailed_info
    }));
  }

  clearCalculations(): void {
    this.currentCalculationSubject.next(null);
    this.currentInputDataSubject.next(null);
  }

  getCurrentInputData(): PensionInputData | null {
    return this.currentInputDataSubject.value;
  }

  getCurrentCalculation(): PensionCalculationResult | null {
    return this.currentCalculationSubject.value;
  }
}