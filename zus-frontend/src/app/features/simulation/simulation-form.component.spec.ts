import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SimulationFormComponent } from './simulation-form.component';

describe('SimulationFormComponent', () => {
  let component: SimulationFormComponent;
  let fixture: ComponentFixture<SimulationFormComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SimulationFormComponent]
    });
    fixture = TestBed.createComponent(SimulationFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
