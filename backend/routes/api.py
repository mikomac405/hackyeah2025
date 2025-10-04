from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
import pandas as pd
import numpy as np
import os
import json
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
