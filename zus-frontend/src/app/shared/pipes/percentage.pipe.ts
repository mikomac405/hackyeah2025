import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'percentage',
  standalone: false
})
export class PercentagePipe implements PipeTransform {
  transform(value: number | null | undefined, decimals: number = 1): string {
    if (value == null) return '';
    
    return new Intl.NumberFormat('pl-PL', {
      style: 'percent',
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    }).format(value / 100);
  }
}