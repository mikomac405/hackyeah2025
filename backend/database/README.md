# Database Module

This module provides an abstraction layer for database operations, making it easy to switch between different database implementations.

## Architecture

The module follows the **Repository Pattern** for clean separation between business logic and data access:

- **`repository.py`**: Abstract base class defining the database interface
- **`sqlite_repository.py`**: SQLite implementation of the repository
- **`factory.py`**: Factory pattern for creating repository instances
- **`__init__.py`**: Module initialization and exports

## Usage

### Basic Usage

```python
from database.factory import get_db

# Get database instance (singleton)
db = get_db()

# Create a simulation
simulation_id = db.create_simulation({
    'age': 30,
    'sex': 'male',
    'gross_salary': 5000,
    'work_start_year': 2015
})

# Get simulation by ID
simulation = db.get_simulation(simulation_id)

# Update simulation with results
db.update_simulation(simulation_id, {
    'actual_amount': 2500,
    'real_amount': 2000
})

# Get all simulations
simulations = db.get_all_simulations(limit=10, offset=0)

# Get statistics
stats = db.get_statistics()
```

## Configuration

### Environment Variables

- **`DB_TYPE`**: Database type (default: `sqlite`)
  - Currently supported: `sqlite`
  - Future: `postgres`, `mysql`, etc.

- **`DB_PATH`**: Path to SQLite database file (default: `pension_simulator.db`)

### Example Configuration

```bash
export DB_TYPE=sqlite
export DB_PATH=/var/data/pension_simulator.db
```

## Database Schema

### Simulations Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key (auto-increment) |
| `timestamp` | TEXT | ISO format timestamp of simulation |
| `status` | TEXT | Status: 'processing', 'completed', 'failed' |
| `input_data` | TEXT | JSON string of input parameters |
| `results` | TEXT | JSON string of calculation results |
| `created_at` | TEXT | ISO format timestamp of record creation |
| `updated_at` | TEXT | ISO format timestamp of last update |

### Indexes

- `idx_timestamp`: Index on timestamp for date range queries
- `idx_status`: Index on status for filtering

## API Endpoints

### Admin Routes (`/api/admin/*`)

#### Get Statistics
```
GET /api/admin/stats
```
Returns database statistics including total simulations, status breakdown, and activity metrics.

#### List Simulations
```
GET /api/admin/simulations?limit=50&offset=0
```
Lists all simulations with pagination.

#### Delete Simulation
```
DELETE /api/admin/simulations/<id>
```
Deletes a specific simulation by ID.

#### Get Simulations by Date Range
```
GET /api/admin/simulations/by-date-range?start_date=2025-01-01&end_date=2025-12-31
```
Returns simulations within a date range.

#### Clear All Simulations
```
POST /api/admin/simulations/clear
Body: {"confirm": "DELETE_ALL"}
```
Clears all simulations (requires confirmation).

#### Database Health Check
```
GET /api/admin/health
```
Checks database connectivity and health.

#### Backup Information
```
GET /api/admin/backup-info
```
Returns information about the database file for backup purposes.

## Adding a New Database Implementation

To add support for a new database (e.g., PostgreSQL):

1. Create a new file `postgres_repository.py`:
```python
from .repository import Repository

class PostgresRepository(Repository):
    def __init__(self, connection_string):
        # Initialize PostgreSQL connection
        pass
    
    # Implement all abstract methods from Repository
    def create_simulation(self, input_data):
        pass
    
    # ... etc
```

2. Update `factory.py`:
```python
elif db_type == 'postgres':
    connection_string = kwargs.get('connection_string')
    return PostgresRepository(connection_string=connection_string)
```

3. Set environment variable:
```bash
export DB_TYPE=postgres
export DB_CONNECTION_STRING="postgresql://user:pass@localhost/dbname"
```

## Testing

The database layer is designed to be easily testable:

```python
from database.factory import DatabaseFactory

# Create a test instance with in-memory database
test_db = DatabaseFactory.create_repository('sqlite', db_path=':memory:')

# Run tests
simulation_id = test_db.create_simulation({'age': 30})
assert simulation_id > 0

# Clean up
DatabaseFactory.reset()
```

## Migration from In-Memory Storage

The module automatically migrates from the previous in-memory storage system. All routes have been updated to use the database abstraction layer.

### Changes:
- ✅ Removed `simulations_db = []` from `routes/api.py`
- ✅ All routes now use `get_db()` to access the database
- ✅ Data persists between application restarts
- ✅ Admin routes added for database management

## Backup and Maintenance

### SQLite Backup

To backup the SQLite database:
```bash
# Simple file copy
cp pension_simulator.db pension_simulator.db.backup

# Or use SQLite backup command
sqlite3 pension_simulator.db ".backup pension_simulator.db.backup"
```

### Database Location

By default, the database file is created in the backend directory. For production, set `DB_PATH` to a persistent location:
```bash
export DB_PATH=/var/lib/pension-simulator/database.db
```

## Performance Considerations

- Indexes are created on `timestamp` and `status` columns for faster queries
- Connection pooling is handled automatically by SQLite
- For high-traffic applications, consider switching to PostgreSQL or MySQL

## Security Notes

- 🔒 Admin routes should be protected with authentication in production
- 🔒 Database credentials should never be hardcoded
- 🔒 Use environment variables for sensitive configuration
- 🔒 Regular backups should be automated
