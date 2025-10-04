"""
SQLite implementation of the repository pattern
"""

import sqlite3
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from contextlib import contextmanager
from .repository import Repository


class SQLiteRepository(Repository):
    """SQLite implementation of the database repository"""

    def __init__(self, db_path: str = 'pension_simulator.db'):
        """
        Initialize SQLite repository
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.initialize()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def initialize(self):
        """Create tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS simulations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    status TEXT NOT NULL,
                    input_data TEXT NOT NULL,
                    results TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # Create indexes for common queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON simulations(timestamp)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_status 
                ON simulations(status)
            ''')

    def create_simulation(self, input_data: Dict[str, Any]) -> int:
        """Create a new simulation record"""
        timestamp = datetime.utcnow().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO simulations 
                (timestamp, status, input_data, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                timestamp,
                'processing',
                json.dumps(input_data),
                timestamp,
                timestamp
            ))
            return cursor.lastrowid

    def get_simulation(self, simulation_id: int) -> Optional[Dict[str, Any]]:
        """Get a simulation by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM simulations WHERE id = ?
            ''', (simulation_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_dict(row)
            return None

    def update_simulation(self, simulation_id: int, results: Dict[str, Any], status: str = 'completed') -> bool:
        """Update a simulation with results"""
        timestamp = datetime.utcnow().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE simulations 
                SET results = ?, status = ?, updated_at = ?
                WHERE id = ?
            ''', (
                json.dumps(results),
                status,
                timestamp,
                simulation_id
            ))
            return cursor.rowcount > 0

    def get_all_simulations(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all simulations with optional pagination"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM simulations ORDER BY timestamp DESC'
            
            if limit is not None:
                query += f' LIMIT {limit} OFFSET {offset}'
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            return [self._row_to_dict(row) for row in rows]

    def delete_simulation(self, simulation_id: int) -> bool:
        """Delete a simulation by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM simulations WHERE id = ?', (simulation_id,))
            return cursor.rowcount > 0

    def get_simulation_count(self) -> int:
        """Get the total number of simulations"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as count FROM simulations')
            row = cursor.fetchone()
            return row['count']

    def get_simulations_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get simulations within a date range"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM simulations 
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp DESC
            ''', (start_date.isoformat(), end_date.isoformat()))
            rows = cursor.fetchall()
            
            return [self._row_to_dict(row) for row in rows]

    def clear_all_simulations(self) -> bool:
        """Delete all simulations (use with caution)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM simulations')
            return True

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total count
            cursor.execute('SELECT COUNT(*) as count FROM simulations')
            total_count = cursor.fetchone()['count']
            
            # Count by status
            cursor.execute('''
                SELECT status, COUNT(*) as count 
                FROM simulations 
                GROUP BY status
            ''')
            status_counts = {row['status']: row['count'] for row in cursor.fetchall()}
            
            # Recent activity (last 7 days)
            cursor.execute('''
                SELECT COUNT(*) as count 
                FROM simulations 
                WHERE timestamp >= datetime('now', '-7 days')
            ''')
            recent_count = cursor.fetchone()['count']
            
            # Average calculations per day (last 30 days)
            cursor.execute('''
                SELECT COUNT(*) as count 
                FROM simulations 
                WHERE timestamp >= datetime('now', '-30 days')
            ''')
            last_30_days = cursor.fetchone()['count']
            avg_per_day = last_30_days / 30.0 if last_30_days > 0 else 0
            
            return {
                'total_simulations': total_count,
                'status_breakdown': status_counts,
                'recent_7_days': recent_count,
                'last_30_days': last_30_days,
                'avg_per_day': round(avg_per_day, 2)
            }

    def close(self):
        """Close database connection (connection is managed per operation)"""
        pass

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert a database row to a dictionary"""
        return {
            'id': row['id'],
            'timestamp': row['timestamp'],
            'status': row['status'],
            'input_data': json.loads(row['input_data']),
            'results': json.loads(row['results']) if row['results'] else None,
            'created_at': row['created_at'],
            'updated_at': row['updated_at']
        }
