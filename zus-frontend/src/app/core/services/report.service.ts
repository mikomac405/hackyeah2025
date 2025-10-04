import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { delay } from 'rxjs/operators';
import { PensionCalculationResult, PensionInputData } from '../models/pension-data.model';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

@Injectable({
  providedIn: 'root'
})
export class ReportService {

  constructor() { }

  /**
   * Generuje raport PDF dla użytkownika
   */
  generatePDFReport(
    inputData: PensionInputData, 
    results: PensionCalculationResult
  ): Observable<Blob> {
    
    return new Observable(observer => {
      setTimeout(() => {
        try {
          const pdf = new jsPDF();
          
          // Nagłówek
          pdf.setFontSize(20);
          pdf.text('Raport prognozy emerytury ZUS', 20, 30);
          
          // Dane wejściowe
          pdf.setFontSize(14);
          pdf.text('Dane wejściowe:', 20, 50);
          pdf.setFontSize(12);
          pdf.text(`Wiek: ${inputData.age} lat`, 20, 65);
          pdf.text(`Płeć: ${inputData.gender === 'female' ? 'Kobieta' : 'Mężczyzna'}`, 20, 75);
          pdf.text(`Wynagrodzenie brutto: ${inputData.grossSalary.toLocaleString('pl-PL')} zł`, 20, 85);
          pdf.text(`Rok rozpoczęcia pracy: ${inputData.workStartYear}`, 20, 95);
          
          // Wyniki
          pdf.setFontSize(14);
          pdf.text('Prognoza emerytury:', 20, 115);
          pdf.setFontSize(12);
          pdf.text(`Kwota rzeczywista: ${results.realAmount.toLocaleString('pl-PL')} zł`, 20, 130);
          pdf.text(`Kwota urealniona: ${results.inflationAdjustedAmount.toLocaleString('pl-PL')} zł`, 20, 140);
          pdf.text(`Stopa zastąpienia: ${results.replacementRate}%`, 20, 150);
          
          // Scenariusze
          pdf.setFontSize(14);
          pdf.text('Scenariusze opóźnienia emerytury:', 20, 170);
          pdf.setFontSize(12);
          pdf.text(`+1 rok: ${results.delayedRetirementScenarios.oneYear.amount.toLocaleString('pl-PL')} zł`, 20, 185);
          pdf.text(`+2 lata: ${results.delayedRetirementScenarios.twoYears.amount.toLocaleString('pl-PL')} zł`, 20, 195);
          pdf.text(`+5 lat: ${results.delayedRetirementScenarios.fiveYears.amount.toLocaleString('pl-PL')} zł`, 20, 205);
          
          // Stopka
          pdf.setFontSize(10);
          pdf.text('Raport wygenerowany przez Symulator Emerytalny ZUS', 20, 280);
          pdf.text(`Data: ${new Date().toLocaleDateString('pl-PL')}`, 20, 290);
          
          const blob = new Blob([pdf.output('blob')], { type: 'application/pdf' });
          observer.next(blob);
          observer.complete();
        } catch (error) {
          observer.error(error);
        }
      }, 1500);
    });
  }

  /**
   * Generuje screenshot komponentu jako PNG
   */
  generateScreenshot(elementId: string): Observable<Blob> {
    return new Observable(observer => {
      const element = document.getElementById(elementId);
      if (!element) {
        observer.error('Element not found');
        return;
      }

      html2canvas(element).then((canvas: HTMLCanvasElement) => {
        canvas.toBlob((blob: Blob | null) => {
          if (blob) {
            observer.next(blob);
            observer.complete();
          } else {
            observer.error('Failed to generate screenshot');
          }
        });
      }).catch((error: any) => {
        observer.error(error);
      });
    });
  }

  /**
   * Pobiera szablon raportu
   */
  getReportTemplate(): Observable<string> {
    const template = `
      <div class="report-template">
        <h1>Raport prognozy emerytury</h1>
        <div class="input-section">
          <h2>Dane wejściowe</h2>
          <!-- Dynamiczne dane -->
        </div>
        <div class="results-section">
          <h2>Wyniki prognozy</h2>
          <!-- Dynamiczne wyniki -->
        </div>
      </div>
    `;
    
    return of(template).pipe(delay(100));
  }
}