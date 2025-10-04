from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
import pandas as pd
import numpy as np
import os
import json
from models.pension_calculator import PensionCalculator
from utils.report_generator import generate_report

api_bp = Blueprint('api', __name__)

# In-memory storage (replace with database in production)
simulations_db = []
admin_reports_db = []

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
            'zus_colors': [
                {'r': 255, 'g': 179, 'b': 79},
                {'r': 0, 'g': 153, 'b': 63},
                {'r': 190, 'g': 195, 'b': 206},
                {'r': 63, 'g': 132, 'b': 210},
                {'r': 0, 'g': 65, 'b': 110},
                {'r': 240, 'g': 94, 'b': 94},
                {'r': 0, 'g': 0, 'b': 0}
            ]
        }

        return jsonify(dashboard_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/simulate', methods=['POST'])
def simulate_pension():
    """Calculate pension based on provided parameters"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['age', 'sex', 'gross_salary', 'work_start_year']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Create simulation record
        simulation_id = len(simulations_db) + 1
        simulation_data = {
            'id': simulation_id,
            'timestamp': datetime.utcnow().isoformat(),
            'input_data': data,
            'status': 'processing'
        }

        simulations_db.append(simulation_data)

        # Use pension calculator
        calculator = PensionCalculator()
        result = calculator.calculate_pension(data)

        # Update simulation with results
        simulation_data.update({
            'status': 'completed',
            'results': result
        })

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
        simulation = next((s for s in simulations_db if s['id'] == simulation_id), None)
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

        # Validate simulation_id
        if 'simulation_id' not in data:
            return jsonify({'error': 'simulation_id is required'}), 400

        simulation_id = data['simulation_id']
        simulation = next((s for s in simulations_db if s['id'] == simulation_id), None)
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
        simulation = next((s for s in simulations_db if s['id'] == simulation_id), None)
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
        reports = []

        for sim in simulations_db:
            report_data = {
                'date_of_use': sim['timestamp'].split('T')[0],
                'time_of_use': sim['timestamp'].split('T')[1].split('.')[0],
                'expected_pension': sim['input_data'].get('expected_pension', ''),
                'age': sim['input_data'].get('age', ''),
                'sex': sim['input_data'].get('sex', ''),
                'salary_amount': sim['input_data'].get('gross_salary', ''),
                'include_sick_leave': sim['input_data'].get('include_sick_leave', False),
                'zus_funds': sim['input_data'].get('zus_funds', ''),
                'actual_pension': sim['results'].get('actual_amount', '') if 'results' in sim else '',
                'real_pension': sim['results'].get('real_amount', '') if 'results' in sim else '',
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
