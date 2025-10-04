import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PensionCalculatorService } from '../../core/services/pension-calculator.service';
import { PensionGroup } from '../../core/models/pension-data.model';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  standalone: false
})
export class HomeComponent implements OnInit {
  pensionGroups: PensionGroup[] = [];
  randomFact = '';
  expectedPension = 3000;
  isLoading = true;

  constructor(
    private pensionCalculator: PensionCalculatorService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadPensionGroups();
    this.loadRandomFact();
  }

  loadPensionGroups() {
    this.pensionCalculator.getPensionGroups().subscribe(
      groups => {
        this.pensionGroups = groups;
        this.isLoading = false;
      }
    );
  }

  loadRandomFact() {
    this.pensionCalculator.getRandomFact().subscribe(
      fact => this.randomFact = fact
    );
  }

  startSimulation() {
    this.router.navigate(['/simulation']);
  }
}