import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import math

class PensionCalculator:
    """Pension calculator for Polish ZUS system"""

    def __init__(self):
        # Polish pension system parameters (these would come from ZUS/GUS data in production)
        self.current_year = datetime.now().year
        self.retirement_age_men = 65
        self.retirement_age_women = 60
        self.min_years_men = 25
        self.min_years_women = 20
        self.average_salary_growth = 0.03  # 3% annual growth
        self.inflation_rate = 0.025  # 2.5% annual inflation
        self.pension_indexation = 0.02  # 2% annual indexation

        # Average sick leave days per year (from GUS data)
        self.avg_sick_leave_men = 12
        self.avg_sick_leave_women = 16

    def calculate_pension(self, input_data):
        """Calculate pension based on input parameters"""
        try:
            age = input_data['age']
            sex = input_data['sex'].lower()
            gross_salary = input_data['gross_salary']
            work_start_year = input_data['work_start_year']
            work_end_year = input_data.get('work_end_year',
                self._calculate_retirement_year(age, sex))

            # Optional parameters
            zus_funds = input_data.get('zus_funds', 0)
            include_sick_leave = input_data.get('include_sick_leave', False)

            # Calculate years of work
            years_of_work = work_end_year - work_start_year

            # Validate minimum years
            min_years = self.min_years_men if sex == 'm' else self.min_years_women
            if years_of_work < min_years:
                return {
                    'error': f'Niewystarczające lata pracy. Wymagane minimum: {min_years} lat'
                }

            # Calculate accumulated capital
            accumulated_capital = self._calculate_accumulated_capital(
                gross_salary, work_start_year, work_end_year,
                zus_funds, include_sick_leave, sex
            )

            # Calculate pension amounts
            actual_amount = self._calculate_monthly_pension(accumulated_capital, sex)
            real_amount = self._calculate_real_pension(actual_amount, work_end_year)

            # Calculate replacement rate
            replacement_rate = (actual_amount / gross_salary) * 100

            # Calculate average pension comparison
            avg_pension_year = self._get_average_pension(work_end_year, sex)

            # Calculate deferral benefits
            deferral_benefits = self._calculate_deferral_benefits(
                accumulated_capital, work_end_year, sex
            )

            results = {
                'actual_amount': round(actual_amount, 2),
                'real_amount': round(real_amount, 2),
                'replacement_rate': round(replacement_rate, 2),
                'accumulated_capital': round(accumulated_capital, 2),
                'years_of_work': years_of_work,
                'retirement_year': work_end_year,
                'average_pension_comparison': avg_pension_year,
                'deferral_benefits': deferral_benefits,
                'calculation_details': {
                    'base_salary': gross_salary,
                    'indexation_years': work_end_year - self.current_year,
                    'sick_leave_impact': self._calculate_sick_leave_impact(gross_salary, sex) if include_sick_leave else 0
                }
            }

            return results

        except Exception as e:
            return {'error': f'Błąd kalkulacji: {str(e)}'}

    def _calculate_retirement_year(self, age, sex):
        """Calculate default retirement year based on age and sex"""
        current_year = self.current_year
        birth_year = current_year - age

        retirement_age = self.retirement_age_men if sex == 'm' else self.retirement_age_women
        return birth_year + retirement_age

    def _calculate_accumulated_capital(self, salary, start_year, end_year, zus_funds, include_sick_leave, sex):
        """Calculate accumulated capital in ZUS account"""
        capital = zus_funds

        # Index salary for each year of work
        for year in range(start_year, min(end_year, self.current_year)):
            indexed_salary = salary * ((1 + self.average_salary_growth) ** (self.current_year - year))

            # Apply sick leave reduction if included
            if include_sick_leave:
                sick_leave_reduction = self._get_sick_leave_reduction(sex)
                indexed_salary *= (1 - sick_leave_reduction)

            # ZUS contribution (19.52% of gross salary)
            zus_contribution = indexed_salary * 0.1952
            capital += zus_contribution

        # Project future contributions
        for year in range(max(start_year, self.current_year), end_year):
            projected_salary = salary * ((1 + self.average_salary_growth) ** (year - start_year + 1))

            if include_sick_leave:
                sick_leave_reduction = self._get_sick_leave_reduction(sex)
                projected_salary *= (1 - sick_leave_reduction)

            zus_contribution = projected_salary * 0.1952
            capital += zus_contribution

        return capital

    def _calculate_monthly_pension(self, capital, sex):
        """Calculate monthly pension amount"""
        # Average life expectancy after retirement (based on GUS data)
        life_expectancy = 19.5 if sex == 'm' else 23.8  # years

        # Monthly pension calculation
        monthly_pension = capital / (life_expectancy * 12)

        # Apply minimum pension guarantee (if applicable)
        minimum_pension = 1588.44  # PLN (2024 value)
        return max(monthly_pension, minimum_pension)

    def _calculate_real_pension(self, nominal_amount, retirement_year):
        """Calculate inflation-adjusted pension amount"""
        years_to_retirement = retirement_year - self.current_year
        real_amount = nominal_amount / ((1 + self.inflation_rate) ** years_to_retirement)
        return real_amount

    def _get_average_pension(self, year, sex):
        """Get average pension for comparison"""
        # Mock data - in production, this would come from ZUS statistics
        base_avg = 2500 if sex == 'm' else 2100
        growth_rate = 0.02  # 2% annual growth
        years_diff = year - self.current_year
        return base_avg * ((1 + growth_rate) ** years_diff)

    def _calculate_deferral_benefits(self, capital, retirement_year, sex):
        """Calculate benefits of deferring retirement"""
        deferral_benefits = {}

        for years in [1, 2, 5]:
            deferred_year = retirement_year + years
            deferred_capital = capital * ((1 + 0.08) ** years)  # 8% annual increase for deferral

            deferred_pension = self._calculate_monthly_pension(deferred_capital, sex)
            real_deferred_pension = self._calculate_real_pension(deferred_pension, deferred_year)

            deferral_benefits[f'{years}_years'] = {
                'actual_amount': round(deferred_pension, 2),
                'real_amount': round(real_deferred_pension, 2),
                'increase_percentage': round(((deferred_pension / self._calculate_monthly_pension(capital, sex)) - 1) * 100, 2)
            }

        return deferral_benefits

    def _get_sick_leave_reduction(self, sex):
        """Get sick leave impact on salary"""
        avg_sick_days = self.avg_sick_leave_men if sex == 'm' else self.avg_sick_leave_women
        return (avg_sick_days / 365) * 0.8  # 80% of salary during sick leave

    def _calculate_sick_leave_impact(self, salary, sex):
        """Calculate financial impact of sick leave"""
        avg_sick_days = self.avg_sick_leave_men if sex == 'm' else self.avg_sick_leave_women
        sick_leave_cost = (avg_sick_days / 365) * salary * 0.2  # 20% of salary not covered
        return sick_leave_cost

    def get_advanced_analysis(self, input_data):
        """Get advanced analysis for dashboard"""
        try:
            # Get base simulation results
            base_results = self.calculate_pension(input_data)
            if 'error' in base_results:
                return base_results

            # Calculate scenarios with different parameters
            scenarios = {}

            # Scenario: Higher salary growth
            modified_data = input_data.copy()
            scenarios['higher_salary_growth'] = self._calculate_scenario(
                modified_data, salary_growth_multiplier=1.5
            )

            # Scenario: Lower salary growth
            scenarios['lower_salary_growth'] = self._calculate_scenario(
                modified_data, salary_growth_multiplier=0.7
            )

            # Scenario: Including sick leave if not already included
            if not input_data.get('include_sick_leave', False):
                scenarios['with_sick_leave'] = self._calculate_scenario(
                    modified_data, include_sick_leave=True
                )

            # Historical salary analysis (if provided)
            historical_analysis = {}
            if 'historical_salaries' in input_data:
                historical_analysis = self._analyze_historical_salaries(
                    input_data['historical_salaries']
                )

            return {
                'base_results': base_results,
                'scenarios': scenarios,
                'historical_analysis': historical_analysis,
                'capital_accumulation_projection': self._project_capital_accumulation(input_data)
            }

        except Exception as e:
            return {'error': f'Advanced analysis error: {str(e)}'}

    def _calculate_scenario(self, input_data, **modifications):
        """Calculate pension for modified scenario"""
        scenario_data = input_data.copy()

        for key, value in modifications.items():
            if key == 'salary_growth_multiplier':
                # This would modify the salary growth rate
                pass  # Implementation would adjust the growth rate
            else:
                scenario_data[key] = value

        return self.calculate_pension(scenario_data)

    def _analyze_historical_salaries(self, historical_salaries):
        """Analyze impact of historical salary data"""
        # Mock analysis - in production, would calculate actual impact
        return {
            'average_annual_growth': 0.045,
            'salary_volatility': 0.12,
            'projected_future_salary': historical_salaries[-1] * 1.5
        }

    def _project_capital_accumulation(self, input_data):
        """Project capital accumulation over time"""
        projections = []

        work_start_year = input_data['work_start_year']
        work_end_year = input_data.get('work_end_year',
            self._calculate_retirement_year(input_data['age'], input_data['sex']))

        salary = input_data['gross_salary']

        for year in range(work_start_year, work_end_year + 1):
            years_worked = year - work_start_year + 1
            projected_salary = salary * ((1 + self.average_salary_growth) ** years_worked)

            # Simple projection (in production, would be more sophisticated)
            projected_capital = projected_salary * years_worked * 0.1952 * 0.7  # Rough estimate

            projections.append({
                'year': year,
                'projected_salary': round(projected_salary, 2),
                'projected_capital': round(projected_capital, 2)
            })

        return projections
