import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { PensionCalculatorService } from '../../core/services/pension-calculator.service';
import { PensionInputData } from '../../core/models/pension-data.model';

@Component({
  selector: 'app-simulation-form',
  templateUrl: './simulation-form.component.html',
  styleUrls: ['./simulation-form.component.css'],
  standalone: false
})
export class SimulationFormComponent implements OnInit {
  simulationForm: FormGroup;
  isCalculating = false;

  constructor(
    private fb: FormBuilder,
    private pensionCalculator: PensionCalculatorService,
    private router: Router
  ) {
    this.simulationForm = this.createForm();
  }

  ngOnInit() {}

  private createForm(): FormGroup {
    return this.fb.group({
      age: [30, [Validators.required, Validators.min(18), Validators.max(67)]],
      gender: ['male', Validators.required],
      grossSalary: [5000, [Validators.required, Validators.min(1000)]],
      workStartYear: [2020, [Validators.required, Validators.min(1980)]],
      workEndYear: [''],
      currentFunds: [0, Validators.min(0)],
      sickLeaveImpact: [false],
      expectedPension: ['', Validators.min(0)],
      postalCode: ['']
    });
  }

  onSubmit() {
    if (this.simulationForm.valid) {
      this.isCalculating = true;
      const inputData: PensionInputData = this.simulationForm.value;
      
      this.pensionCalculator.calculatePension(inputData).subscribe(
        result => {
          this.isCalculating = false;
          this.router.navigate(['/results']);
        },
        error => {
          this.isCalculating = false;
          console.error('Błąd kalkulacji:', error);
        }
      );
    }
  }
}
