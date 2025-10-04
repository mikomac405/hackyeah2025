from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
import pandas as pd
import numpy as np
import os
import json
import random
from models.pension_calculator import PensionCalculator
from utils.report_generator import generate_report
from database.factory import get_db

api_bp = Blueprint('api', __name__)

@api_bp.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get basic dashboard data including average pensions and facts"""
    try:
        # Mock data - in production, this would come from ZUS/GUS/NBP data sources
        dashboard_data = {
            'average_pensions': {
                'general': 2500.00,
                'men': 2800.00,
                'women': 2200.00,
                'by_voivodeship': {
                    'śląskie': 2900.00,
                    'mazowieckie': 2700.00,
                    'małopolskie': 2400.00
                }
            },
            'did_you_know': [
                "Najwyższa emerytura w Polsce jest wypłacana mieszkańcowi województwa śląskiego i wynosi 15 000 PLN",
                "Średni czas spędzony na zwolnieniu lekarskim w Polsce to 14 dni w roku",
                "Wysokość emerytury zależy od 80% najlepszych lat pracy"
            ],
        }

        return jsonify(dashboard_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/simulate', methods=['POST'])
def simulate_pension():
    """Calculate pension based on provided parameters"""
    try:
        data = request.get_json()
        db = get_db()

        # Validate required fields
        required_fields = ['age', 'sex', 'gross_salary', 'work_start_year']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Create simulation record in database
        simulation_id = db.create_simulation(data)

        # Use pension calculator
        calculator = PensionCalculator()
        result = calculator.calculate_pension(data)

        # Update simulation with results
        db.update_simulation(simulation_id, result, 'completed')

        return jsonify({
            'simulation_id': simulation_id,
            'results': result
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/simulation/<int:simulation_id>', methods=['GET'])
def get_simulation(simulation_id):
    """Get simulation results by ID"""
    try:
        db = get_db()
        simulation = db.get_simulation(simulation_id)
        if not simulation:
            return jsonify({'error': 'Simulation not found'}), 404

        return jsonify(simulation)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/dashboard-advanced', methods=['POST'])
def advanced_dashboard():
    """Advanced dashboard for detailed analysis"""
    try:
        data = request.get_json()
        db = get_db()

        # Validate simulation_id
        if 'simulation_id' not in data:
            return jsonify({'error': 'simulation_id is required'}), 400

        simulation_id = data['simulation_id']
        simulation = db.get_simulation(simulation_id)
        if not simulation:
            return jsonify({'error': 'Simulation not found'}), 404

        # Advanced calculations
        calculator = PensionCalculator()
        advanced_results = calculator.get_advanced_analysis(simulation['input_data'])

        return jsonify(advanced_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/report/<int:simulation_id>', methods=['GET'])
def download_report(simulation_id):
    """Generate and download pension report"""
    try:
        db = get_db()
        simulation = db.get_simulation(simulation_id)
        if not simulation:
            return jsonify({'error': 'Simulation not found'}), 404

        # Generate report
        report_path = generate_report(simulation)

        return send_file(
            report_path,
            as_attachment=True,
            download_name=f'pension_report_{simulation_id}.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/admin/reports', methods=['GET'])
def get_admin_reports():
    """Get all simulation reports for admin (requires authentication in production)"""
    try:
        # In production, add authentication check here
        db = get_db()
        simulations = db.get_all_simulations()
        reports = []

        for sim in simulations:
            report_data = {
                'date_of_use': sim['timestamp'].split('T')[0],
                'time_of_use': sim['timestamp'].split('T')[1].split('.')[0],
                'expected_pension': sim['input_data'].get('expected_pension', ''),
                'age': sim['input_data'].get('age', ''),
                'sex': sim['input_data'].get('sex', ''),
                'salary_amount': sim['input_data'].get('gross_salary', ''),
                'include_sick_leave': sim['input_data'].get('include_sick_leave', False),
                'zus_funds': sim['input_data'].get('zus_funds', ''),
                'actual_pension': sim['results'].get('actual_amount', '') if sim['results'] else '',
                'real_pension': sim['results'].get('real_amount', '') if sim['results'] else '',
                'postal_code': sim['input_data'].get('postal_code', '')
            }
            reports.append(report_data)

        # Generate Excel file
        df = pd.DataFrame(reports)
        excel_path = f'/tmp/admin_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        df.to_excel(excel_path, index=False)

        return send_file(
            excel_path,
            as_attachment=True,
            download_name='admin_usage_report.xlsx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/random-fact', methods=['GET'])
def get_random_fact():
    """Zwraca losową ciekawostkę o emeryturach"""
    facts = [
        "Średnia emerytura w Polsce wynosi około 2,800 zł brutto.",
        "Kobiety przechodzą na emeryturę w wieku 60 lat, mężczyźni w wieku 65 lat.",
        "Składka emerytalna wynosi 19,52% wynagrodzenia brutto.",
        "System emerytalny w Polsce działa w oparciu o zasadę zdefiniowanej składki.",
        "Minimalna emerytura w 2024 roku wynosi 1,588.44 zł brutto.",
        "Każdy dodatkowy rok pracy może zwiększyć emeryturę nawet o 8-10%.",
        "W 2023 roku średni okres pobierania emerytury wynosił około 22 lata.",
        "Kobiety otrzymują średnio o 25% niższe emerytury niż mężczyźni.",
        "Prognoza demograficzna wskazuje na wzrost liczby emerytów do 2040 roku.",
        "System emerytalny składa się z I filaru (ZUS) i opcjonalnego III filaru (PPK, IKE).",
        "Średni wiek przejścia na emeryturę w Polsce to 61 lat.",
        "Emerytura minimalna jest waloryzowana co roku wraz z inflacją.",
        "Składka emerytalna jest dzielona między ubezpieczonego (9,76%) i pracodawcę (9,76%).",
        "ZUS wypłaca miesięcznie około 9 milionów emerytur i rent.",
        "Emerytury są indeksowane dwa razy w roku - w marcu i wrześniu."
    ]
    
    random_fact = random.choice(facts)
    
    return jsonify({
        "fact": random_fact,
        "timestamp": datetime.now().isoformat()
    })

@api_bp.route('/pension-groups', methods=['GET'])
def get_pension_groups():
    """Zwraca grupy emerytalne do wykresów"""
    groups = [
        {
            "name": "Poniżej minimalnej",
            "description": "Emerytury poniżej minimalnej kwoty",
            "average_amount": 1200,
            "percentage": 15,
            "color": "#F05E5E",
            "detailed_info": "Głównie osoby z krótkimi okresami składkowymi lub niskimi zarobkami. ZUS dopłaca do minimalnej emerytury."
        },
        {
            "name": "Minimalna - 2000 zł",
            "description": "Emerytury w przedziale minimalnym",
            "average_amount": 1600,
            "percentage": 25,
            "color": "#FFB34F",
            "detailed_info": "Osoby pracujące za najniższą krajową lub z przerwami w karierze zawodowej."
        },
        {
            "name": "2000 - 3500 zł",
            "description": "Średnie emerytury pracowników",
            "average_amount": 2750,
            "percentage": 35,
            "color": "#00993F",
            "detailed_info": "Największa grupa emerytów - osoby ze średnimi zarobkami i regularną aktywnością zawodową."
        },
        {
            "name": "3500 - 5000 zł",
            "description": "Emerytury wyższe",
            "average_amount": 4250,
            "percentage": 20,
            "color": "#3F84D2",
            "detailed_info": "Osoby z długim stażem pracy i ponadprzeciętnymi zarobkami, specjaliści, kierownicy średniego szczebla."
        },
        {
            "name": "Powyżej 5000 zł",
            "description": "Najwyższe emerytury",
            "average_amount": 6500,
            "percentage": 5,
            "color": "#00416E",
            "detailed_info": "Kadra kierownicza, specjaliści z bardzo wysokimi zarobkami, osoby z maksymalnym okresem składkowym."
        }
    ]
    
    return jsonify(groups)

@api_bp.route('/test-calculation', methods=['POST'])
def test_calculation():
    """Test endpoint z minimalnymi danymi"""
    try:
        data = request.get_json()
        print(f"🔍 TEST - Raw data received: {data}")
        
        # Bardzo proste dane testowe
        test_data = {
            'age': 30,
            'sex': 'm',
            'gross_salary': 5000,
            'work_start_year': 2020,
            'work_end_year': 2065,
            'zus_funds': 0,
            'include_sick_leave': False
        }
        
        print(f"🔍 TEST - Using test data: {test_data}")
        
        calculator = PensionCalculator()
        result = calculator.calculate_pension(test_data)
        
        print(f"🔍 TEST - Calculator result: {result}")
        
        return jsonify({
            'test_data_used': test_data,
            'calculation_result': result,
            'status': 'success'
        })
        
    except Exception as e:
        import traceback
        print(f"❌ TEST ERROR: {str(e)}")
        print(f"❌ TEST TRACEBACK: {traceback.format_exc()}")
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@api_bp.route('/calculate-pension', methods=['POST'])
def calculate_pension():
    """Endpoint zgodny z frontendem - mapuje na istniejący /simulate"""
    try:
        data = request.get_json()
        
        # Mapowanie z frontend format (camelCase) na backend format (snake_case)
        gender_mapping = {'male': 'm', 'female': 'f'}  # Mapowanie gender format
        
        try:
            mapped_data = {
                'age': int(data.get('age')) if data.get('age') is not None else None,
                'sex': gender_mapping.get(data.get('gender'), data.get('gender')),  # Mapowanie male/female -> m/f
                'gross_salary': float(data.get('grossSalary')) if data.get('grossSalary') is not None else None,
                'work_start_year': int(data.get('workStartYear')) if data.get('workStartYear') is not None else None,
                'work_end_year': int(data.get('workEndYear')) if data.get('workEndYear') and data.get('workEndYear') != '' else None,
                'zus_funds': float(data.get('currentFunds', 0)),  # Backend oczekuje 'zus_funds'
                'include_sick_leave': bool(data.get('sickLeaveImpact', False)),  # Backend oczekuje 'include_sick_leave'
                'expected_pension': float(data.get('expectedPension')) if data.get('expectedPension') else None,
                'postal_code': data.get('postalCode')  # Poprawiono: camelCase z frontend
            }
        except (ValueError, TypeError) as conversion_error:
            print(f"❌ Data conversion error: {str(conversion_error)}")
            return jsonify({'error': f'Invalid data format: {str(conversion_error)}'}), 400
        
        # DEBUG: Loguj zmapowane dane
        print("🔍 DEBUG - Mapped data for backend:")
        for key, value in mapped_data.items():
            print(f"  {key}: {value} (type: {type(value)})")
        
        # Validate required fields
        required_fields = ['age', 'sex', 'gross_salary', 'work_start_year']
        for field in required_fields:
            if field not in mapped_data or mapped_data[field] is None or mapped_data[field] == '':
                print(f"❌ Validation failed for field: {field} = {mapped_data.get(field)}")
                return jsonify({'error': f'Missing required field: {field}'}), 400

        try:
            db = get_db()
            simulation_id = db.create_simulation(mapped_data)
        except Exception as db_error:
            print(f"❌ Database error: {str(db_error)}")
            import traceback
            print(f"❌ Database traceback: {traceback.format_exc()}")
            # Continue without database for now
            simulation_id = None

        try:
            calculator = PensionCalculator()
            result = calculator.calculate_pension(mapped_data)
            
            # DEBUG: Sprawdź czy są błędy w kalkulatorze
            if isinstance(result, dict) and 'error' in result:
                print(f"❌ Backend calculator error: {result['error']}")
                return jsonify({'error': f"Calculator error: {result['error']}"}), 500
            
            # DEBUG: Loguj wynik kalkulatora
            print("🔍 DEBUG - Backend calculator result:")
            print(f"  actual_amount: {result.get('actual_amount')}")
            print(f"  real_amount: {result.get('real_amount')}")
            print(f"  replacement_rate: {result.get('replacement_rate')}")
            print(f"  deferral_benefits keys: {result.get('deferral_benefits', {}).keys()}")
            print(f"  full result keys: {result.keys()}")
            print(f"  full result: {result}")

            if simulation_id:
                try:
                    db.update_simulation(simulation_id, result, 'completed')
                except Exception as db_update_error:
                    print(f"⚠️ Database update error (continuing anyway): {str(db_update_error)}")
            
        except Exception as calc_error:
            print(f"❌ Exception in calculator: {str(calc_error)}")
            print(f"❌ Calculator exception type: {type(calc_error)}")
            import traceback
            print(f"❌ Full traceback: {traceback.format_exc()}")
            return jsonify({'error': f"Calculator exception: {str(calc_error)}"}), 500

        # Mapowanie z backend format na frontend format
        frontend_result = {
            'real_amount': result.get('actual_amount', 0),
            'inflation_adjusted_amount': result.get('real_amount', 0),
            'replacement_rate': result.get('replacement_rate', 0),
            'average_pension_comparison': result.get('average_pension_comparison', 0),  # Poprawiono nazewnictwo
            'delayed_retirement_scenarios': {
                'one_year': {
                    'amount': result.get('deferral_benefits', {}).get('1_years', {}).get('actual_amount', 0),
                    'increase': result.get('deferral_benefits', {}).get('1_years', {}).get('increase_percentage', 0)
                },
                'two_years': {
                    'amount': result.get('deferral_benefits', {}).get('2_years', {}).get('actual_amount', 0),
                    'increase': result.get('deferral_benefits', {}).get('2_years', {}).get('increase_percentage', 0)
                },
                'five_years': {
                    'amount': result.get('deferral_benefits', {}).get('5_years', {}).get('actual_amount', 0),
                    'increase': result.get('deferral_benefits', {}).get('5_years', {}).get('increase_percentage', 0)
                }
            },
            'funds_growth_timeline': result.get('capital_accumulation_projection', [])  # Poprawiono nazewnictwo
        }
        
        if 'sick_leave_impact' in result:
            frontend_result['sick_leave_impact'] = {
                'with_sick_leave': result['sick_leave_impact'].get('with_sick_leave', 0),
                'without_sick_leave': result['sick_leave_impact'].get('without_sick_leave', 0),
                'difference': result['sick_leave_impact'].get('difference', 0),
                'percentage_impact': result['sick_leave_impact'].get('percentage_impact', 0)
            }

        return jsonify(frontend_result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Sprawdza status backend"""
    return jsonify({
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "service": "ZUS Pension Calculator Backend"
    })

@api_bp.route('/regional-stats', methods=['GET'])
def get_regional_stats():
    """Zwraca statystyki regionalne"""
    postal_code = request.args.get('postal_code')
    
    # Mock data na podstawie kodu pocztowego
    base_pension = 2800
    if postal_code:
        region_code = postal_code[:2] if len(postal_code) >= 2 else "00"
        # Symulacja różnic regionalnych
        adjustment = hash(region_code) % 400 - 200
        region_name = f"Województwo {region_code}"
    else:
        adjustment = 0
        region_name = "Cała Polska"
    
    return jsonify({
        "region": region_name,
        "average_pension": base_pension + adjustment,
        "participants_count": 1000 + (hash(postal_code or "") % 500),
        "median_age": 45 + (hash(postal_code or "") % 10)
    })

@api_bp.route('/historical-data', methods=['GET'])
def get_historical_data():
    """Zwraca dane historyczne"""
    return jsonify({
        "years": [2020, 2021, 2022, 2023, 2024],
        "average_salaries": [4500, 4650, 4800, 4950, 5100],
        "inflation_rates": [2.8, 3.2, 2.5, 3.1, 2.9],
        "pension_fund_growth": [1.5, 2.1, 1.8, 2.3, 1.9]
    })

@api_bp.route('/log-usage', methods=['POST'])
def log_usage():
    """Loguje użycie aplikacji"""
    try:
        data = request.get_json()
        # W przyszłości można tu dodać zapis do bazy danych
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
