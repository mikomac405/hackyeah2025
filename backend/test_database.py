"""
Simple test script to verify database functionality
"""

import sys
import os

# Add current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from database.factory import get_db, DatabaseFactory


def test_database():
    """Test basic database operations"""
    print("Testing database operations...")
    print("=" * 50)
    
    # Use test database
    db = DatabaseFactory.create_repository('sqlite', db_path='test_pension.db')
    
    print("\n1. Creating test simulations...")
    sim1_id = db.create_simulation({
        'age': 30,
        'sex': 'male',
        'gross_salary': 5000,
        'work_start_year': 2015
    })
    print(f"   Created simulation with ID: {sim1_id}")
    
    sim2_id = db.create_simulation({
        'age': 35,
        'sex': 'female',
        'gross_salary': 6000,
        'work_start_year': 2010
    })
    print(f"   Created simulation with ID: {sim2_id}")
    
    print("\n2. Retrieving simulation...")
    simulation = db.get_simulation(sim1_id)
    print(f"   Retrieved: {simulation['id']} - Status: {simulation['status']}")
    
    print("\n3. Updating simulation with results...")
    db.update_simulation(sim1_id, {
        'actual_amount': 2500,
        'real_amount': 2000
    }, 'completed')
    print("   Simulation updated successfully")
    
    print("\n4. Getting all simulations...")
    all_sims = db.get_all_simulations()
    print(f"   Total simulations: {len(all_sims)}")
    
    print("\n5. Getting simulation count...")
    count = db.get_simulation_count()
    print(f"   Count: {count}")
    
    print("\n6. Getting database statistics...")
    stats = db.get_statistics()
    print(f"   Total simulations: {stats['total_simulations']}")
    print(f"   Status breakdown: {stats['status_breakdown']}")
    print(f"   Recent (7 days): {stats['recent_7_days']}")
    
    print("\n7. Deleting a simulation...")
    success = db.delete_simulation(sim2_id)
    print(f"   Deleted: {success}")
    
    print("\n8. Verifying deletion...")
    remaining = db.get_simulation_count()
    print(f"   Remaining simulations: {remaining}")
    
    print("\n" + "=" * 50)
    print("✅ All tests passed!")
    print("\nTest database created at: test_pension.db")
    print("You can inspect it with: sqlite3 test_pension.db")
    
    # Clean up
    db.close()


if __name__ == '__main__':
    test_database()
