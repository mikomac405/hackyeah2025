import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, finalize } from 'rxjs/operators';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable()
export class ApiInterceptor implements HttpInterceptor {

  private activeRequests = 0;

  constructor(private snackBar: MatSnackBar) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    this.activeRequests++;

    // Dodaj headers
    const apiReq = req.clone({
      setHeaders: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    });

    return next.handle(apiReq).pipe(
      catchError((error: HttpErrorResponse) => {
        console.error('🚨 HTTP Error:', error);
        
        let errorMessage = 'Wystąpił błąd połączenia z backend';
        
        if (error.status === 0) {
          errorMessage = '❌ Brak połączenia z backend! Sprawdź czy backend jest uruchomiony na porcie 5000.';
        } else if (error.status === 404) {
          errorMessage = '❌ Endpoint nie istnieje w backend API.';
        } else if (error.status === 400) {
          errorMessage = '❌ Błędne dane wejściowe - sprawdź formularz.';
        } else if (error.status === 500) {
          errorMessage = '❌ Błąd wewnętrzny backend - sprawdź logi Python.';
        } else if (error.status === 422) {
          errorMessage = '❌ Błąd walidacji danych w backend.';
        }

        this.snackBar.open(errorMessage, 'Zamknij', {
          duration: 8000,
          panelClass: ['error-snackbar']
        });

        return throwError(() => error);
      }),
      finalize(() => {
        this.activeRequests--;
      })
    );
  }
}