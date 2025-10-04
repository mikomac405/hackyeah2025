"""
Admin routes for database management
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from database.factory import get_db

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/stats', methods=['GET'])
def get_statistics():
    """Get database statistics"""
    try:
        db = get_db()
        stats = db.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/simulations', methods=['GET'])
def list_simulations():
    """List all simulations with pagination"""
    try:
        db = get_db()
        
        # Get pagination parameters
        limit = request.args.get('limit', type=int, default=50)
        offset = request.args.get('offset', type=int, default=0)
        
        simulations = db.get_all_simulations(limit=limit, offset=offset)
        total_count = db.get_simulation_count()
        
        return jsonify({
            'simulations': simulations,
            'total': total_count,
            'limit': limit,
            'offset': offset
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/simulations/<int:simulation_id>', methods=['DELETE'])
def delete_simulation(simulation_id):
    """Delete a specific simulation"""
    try:
        db = get_db()
        
        # Check if simulation exists
        simulation = db.get_simulation(simulation_id)
        if not simulation:
            return jsonify({'error': 'Simulation not found'}), 404
        
        # Delete simulation
        success = db.delete_simulation(simulation_id)
        
        if success:
            return jsonify({
                'message': f'Simulation {simulation_id} deleted successfully'
            })
        else:
            return jsonify({'error': 'Failed to delete simulation'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/simulations/by-date-range', methods=['GET'])
def get_simulations_by_date():
    """Get simulations within a date range"""
    try:
        db = get_db()
        
        # Get date range parameters
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        if not start_date_str or not end_date_str:
            return jsonify({
                'error': 'Both start_date and end_date are required (format: YYYY-MM-DD)'
            }), 400
        
        try:
            start_date = datetime.fromisoformat(start_date_str)
            end_date = datetime.fromisoformat(end_date_str)
        except ValueError:
            return jsonify({
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }), 400
        
        simulations = db.get_simulations_by_date_range(start_date, end_date)
        
        return jsonify({
            'simulations': simulations,
            'count': len(simulations),
            'start_date': start_date_str,
            'end_date': end_date_str
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/simulations/clear', methods=['POST'])
def clear_all_simulations():
    """
    Clear all simulations from database (DANGER: This cannot be undone!)
    Requires confirmation in request body
    """
    try:
        data = request.get_json()
        
        # Require explicit confirmation
        if not data or data.get('confirm') != 'DELETE_ALL':
            return jsonify({
                'error': 'Confirmation required. Send {"confirm": "DELETE_ALL"} to proceed.'
            }), 400
        
        db = get_db()
        count_before = db.get_simulation_count()
        
        success = db.clear_all_simulations()
        
        if success:
            return jsonify({
                'message': 'All simulations cleared successfully',
                'deleted_count': count_before
            })
        else:
            return jsonify({'error': 'Failed to clear simulations'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/health', methods=['GET'])
def database_health():
    """Check database health and connectivity"""
    try:
        db = get_db()
        
        # Try to get count to verify database is accessible
        count = db.get_simulation_count()
        
        return jsonify({
            'status': 'healthy',
            'database_accessible': True,
            'total_records': count,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database_accessible': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500


@admin_bp.route('/backup-info', methods=['GET'])
def backup_info():
    """Get information about database backup"""
    try:
        db = get_db()
        stats = db.get_statistics()
        
        # Get database file info if using SQLite
        from database.sqlite_repository import SQLiteRepository
        if isinstance(db, SQLiteRepository):
            import os
            db_path = db.db_path
            file_exists = os.path.exists(db_path)
            file_size = os.path.getsize(db_path) if file_exists else 0
            
            return jsonify({
                'database_type': 'SQLite',
                'database_path': db_path,
                'file_exists': file_exists,
                'file_size_bytes': file_size,
                'file_size_mb': round(file_size / (1024 * 1024), 2),
                'total_records': stats['total_simulations'],
                'backup_recommendation': 'Copy the database file to backup location'
            })
        else:
            return jsonify({
                'database_type': 'Other',
                'total_records': stats['total_simulations'],
                'backup_recommendation': 'Use database-specific backup tools'
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
