import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'currencyPln',
  standalone: false
})
export class CurrencyPlnPipe implements PipeTransform {
  transform(value: number | null | undefined): string {
    if (value == null) return '';
    
    return new Intl.NumberFormat('pl-PL', {
      style: 'currency',
      currency: 'PLN',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  }
}