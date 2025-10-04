import { Injectable } from '@angular/core';
import { Observable, of, BehaviorSubject } from 'rxjs';
import { delay, map } from 'rxjs/operators';
import { 
  PensionInputData, 
  PensionCalculationResult, 
  PensionGroup 
} from '../models/pension-data.model';

@Injectable({
  providedIn: 'root'
})
export class PensionCalculatorService {
  private readonly CURRENT_YEAR = 2025;
  private readonly AVERAGE_PENSION = 2800;
  private readonly MINIMUM_PENSION = 1588.44;
  private readonly PENSION_CONTRIBUTION_RATE = 0.1952;
  private readonly INFLATION_RATE = 0.025;
  
  // BehaviorSubject do przechowywania aktualnych obliczeń
  private currentCalculationSubject = new BehaviorSubject<PensionCalculationResult | null>(null);
  public currentCalculation$ = this.currentCalculationSubject.asObservable();

  // BehaviorSubject do przechowywania danych wejściowych
  private currentInputDataSubject = new BehaviorSubject<PensionInputData | null>(null);
  public currentInputData$ = this.currentInputDataSubject.asObservable();

  constructor() { }

  /**
   * Główna metoda kalkulacji emerytury
   */
  calculatePension(inputData: PensionInputData): Observable<PensionCalculationResult> {
    // Zapisujemy dane wejściowe
    this.currentInputDataSubject.next(inputData);
    
    return of(this.performCalculation(inputData)).pipe(
      delay(1500), // Symulacja czasu obliczeń
      map(result => {
        this.currentCalculationSubject.next(result);
        return result;
      })
    );
  }

  /**
   * Pobiera grupy emerytalne do wykresu  DO ZMIANY NA SERWIS API
   */
  getPensionGroups(): Observable<PensionGroup[]> {
    const groups: PensionGroup[] = [
      {
        name: 'Poniżej minimalnej',
        description: 'Emerytury poniżej minimalnej kwoty',
        averageAmount: 1200,
        percentage: 15,
        color: '#F05E5E',
        detailedInfo: 'Głównie osoby z krótkimi okresami składkowymi lub niskimi zarobkami. ZUS dopłaca do minimalnej emerytury.'
      },
      {
        name: 'Minimalna - 2000 zł',
        description: 'Emerytury w przedziale minimalnym',
        averageAmount: 1600,
        percentage: 25,
        color: '#FFB34F',
        detailedInfo: 'Osoby pracujące za najniższą krajową lub z przerwami w karierze zawodowej.'
      },
      {
        name: '2000 - 3500 zł',
        description: 'Średnie emerytury pracowników',
        averageAmount: 2750,
        percentage: 35,
        color: '#00993F',
        detailedInfo: 'Największa grupa emerytów - osoby ze średnimi zarobkami i regularną aktywnością zawodową.'
      },
      {
        name: '3500 - 5000 zł',
        description: 'Emerytury wyższe',
        averageAmount: 4250,
        percentage: 20,
        color: '#3F84D2',
        detailedInfo: 'Osoby z długim stażem pracy i ponadprzeciętnymi zarobkami, specjaliści, kierownicy średniego szczebla.'
      },
      {
        name: 'Powyżej 5000 zł',
        description: 'Najwyższe emerytury',
        averageAmount: 6500,
        percentage: 5,
        color: '#00416E',
        detailedInfo: 'Kadra kierownicza, specjaliści z bardzo wysokimi zarobkami, osoby z maksymalnym okresem składkowym.'
      }
    ];

    return of(groups).pipe(delay(300));
  }

  /**
   * Pobiera losową ciekawostkę
   */
  getRandomFact(): Observable<string> {
    const facts = [
      'Średnia emerytura w Polsce wynosi około 2,800 zł brutto.',
      'Kobiety przechodzą na emeryturę w wieku 60 lat, mężczyźni w wieku 65 lat.',
      'Składka emerytalna wynosi 19,52% wynagrodzenia brutto.',
      'System emerytalny w Polsce działa w oparciu o zasadę zdefiniowanej składki.',
      'Minimalna emerytura w 2025 roku wynosi 1,588.44 zł brutto.',
      'Każdy dodatkowy rok pracy może zwiększyć emeryturę nawet o 8-10%.',
      'W 2023 roku średni okres pobierania emerytury wynosił około 22 lata.',
      'Kobiety otrzymują średnio o 25% niższe emerytury niż mężczyźni.',
      'Prognoza demograficzna wskazuje na wzrost liczby emerytów do 2040 roku.',
      'System emerytalny składa się z I filaru (ZUS) i opcjonalnego III filaru (PPK, IKE).',
      'Średni wiek przejścia na emeryturę w Polsce to 61 lat.',
      'Emerytura minimalna jest waloryzowana co roku wraz z inflacją.'
    ];

    const randomFact = facts[Math.floor(Math.random() * facts.length)];
    return of(randomFact).pipe(delay(100));
  }

  /**
   * Czyści zapisane dane
   */
  clearCalculations(): void {
    this.currentCalculationSubject.next(null);
    this.currentInputDataSubject.next(null);
  }

  /**
   * Pobiera aktualne dane wejściowe (synchronicznie)
   */
  getCurrentInputData(): PensionInputData | null {
    return this.currentInputDataSubject.value;
  }

  /**
   * Pobiera aktualne wyniki (synchronicznie)
   */
  getCurrentCalculation(): PensionCalculationResult | null {
    return this.currentCalculationSubject.value;
  }

  /**
   * Prywatna metoda wykonująca obliczenia
   */
  private performCalculation(inputData: PensionInputData): PensionCalculationResult {
    const retirementAge = this.getRetirementAge(inputData.gender);
    const effectiveWorkEndYear = inputData.workEndYear || 
      (this.CURRENT_YEAR + Math.max(0, retirementAge - inputData.age));
    
    const workYears = Math.max(0, effectiveWorkEndYear - inputData.workStartYear);
    const annualContribution = inputData.grossSalary * this.PENSION_CONTRIBUTION_RATE * 12;
    const totalContributions = (annualContribution * workYears) + (inputData.currentFunds || 0);
    
    // Średnia długość życia po przejściu na emeryturę (w miesiącach)
    const averageLifeExpectancy = inputData.gender === 'female' ? 25 * 12 : 20 * 12;
    const basicPension = totalContributions / averageLifeExpectancy;
    
    // Symulacja inflacji
    const yearsToRetirement = Math.max(0, retirementAge - inputData.age);
    const inflationAdjusted = basicPension / Math.pow(1 + this.INFLATION_RATE, yearsToRetirement);
    
    // Wpływ chorobowego (statystycznie kobiety więcej dni chorobowego)
    const sickLeaveImpact = inputData.sickLeaveImpact ? {
      withSickLeave: basicPension,
      withoutSickLeave: basicPension * (inputData.gender === 'female' ? 1.07 : 1.05),
      difference: basicPension * (inputData.gender === 'female' ? 0.07 : 0.05),
      percentageImpact: inputData.gender === 'female' ? 7 : 5
    } : undefined;

    // Scenariusze opóźnienia emerytury
    const delayedRetirementScenarios = {
      oneYear: {
        amount: Math.round(basicPension * 1.08),
        increase: Math.round(basicPension * 0.08)
      },
      twoYears: {
        amount: Math.round(basicPension * 1.16),
        increase: Math.round(basicPension * 0.16)
      },
      fiveYears: {
        amount: Math.round(basicPension * 1.4),
        increase: Math.round(basicPension * 0.4)
      }
    };

    // Timeline wzrostu środków
    const fundsGrowthTimeline = this.calculateFundsGrowthTimeline(
      inputData, workYears, annualContribution
    );

    // Wymagane przedłużenie pracy jeśli emerytura nie spełnia oczekiwań
    let requiredWorkExtension: number | undefined;
    if (inputData.expectedPension && basicPension < inputData.expectedPension) {
      const shortfall = inputData.expectedPension - basicPension;
      requiredWorkExtension = Math.ceil(shortfall / (annualContribution / averageLifeExpectancy));
    }

    return {
      realAmount: Math.round(basicPension),
      inflationAdjustedAmount: Math.round(inflationAdjusted),
      replacementRate: Math.round((basicPension / inputData.grossSalary) * 100),
      averagePensionComparison: Math.round((basicPension / this.AVERAGE_PENSION) * 100),
      sickLeaveImpact,
      delayedRetirementScenarios,
      requiredWorkExtension,
      fundsGrowthTimeline
    };
  }

  private calculateFundsGrowthTimeline(
    inputData: PensionInputData, 
    workYears: number, 
    annualContribution: number
  ): Array<{year: number; age: number; totalFunds: number; annualContribution: number}> {
    const timeline = [];
    const startingFunds = inputData.currentFunds || 0;
    let cumulativeFunds = startingFunds;
    
    for (let i = 0; i <= workYears; i++) {
      const year = inputData.workStartYear + i;
      const age = inputData.age + (year - this.CURRENT_YEAR);
      
      if (i > 0) {
        cumulativeFunds += annualContribution;
      }
      
      timeline.push({
        year,
        age,
        totalFunds: Math.round(cumulativeFunds),
        annualContribution: Math.round(annualContribution)
      });
    }
    
    return timeline;
  }

  private getRetirementAge(gender: string): number {
    return gender === 'female' ? 60 : 65;
  }
}