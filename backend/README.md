# Pension Simulator Backend

Flask REST API for the Polish ZUS Pension Simulator - an educational tool for forecasting pension amounts.

## Features

- **Basic Dashboard**: Pension amount input and comparison with averages
- **Pension Simulation**: Calculate pension based on personal data
- **Advanced Analysis**: Detailed scenarios and projections
- **Report Generation**: PDF reports for simulation results
- **Admin Reports**: Excel reports for usage statistics

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /health` - Check API status

### Dashboard
- `GET /api/dashboard` - Get basic dashboard data (averages, facts, colors)

### Pension Simulation
- `POST /api/simulate` - Calculate pension based on input data
- `GET /api/simulation/{id}` - Get simulation results by ID

### Advanced Analysis
- `POST /api/dashboard-advanced` - Get advanced analysis for existing simulation

### Reports
- `GET /api/report/{id}` - Download PDF report for simulation
- `GET /api/admin/reports` - Download admin usage report (Excel)

## Data Input Format

### Basic Simulation Input:
```json
{
  "age": 35,
  "sex": "M",
  "gross_salary": 5000,
  "work_start_year": 2010,
  "work_end_year": 2045,
  "zus_funds": 50000,
  "include_sick_leave": true,
  "expected_pension": 3000,
  "postal_code": "00-001"
}
```

### Required Fields:
- `age`: Current age
- `sex`: "M" or "F"
- `gross_salary`: Gross monthly salary in PLN
- `work_start_year`: Year work started

### Optional Fields:
- `work_end_year`: Planned retirement year (defaults to statutory retirement age)
- `zus_funds`: Current funds in ZUS account
- `include_sick_leave`: Whether to include sick leave impact
- `expected_pension`: Expected pension amount for comparison
- `postal_code`: Postal code for statistics

## Development

### Project Structure:
```
backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── routes/
│   ├── api.py            # API endpoints
│   └── __init__.py
├── models/
│   ├── pension_calculator.py  # Pension calculation logic
│   └── __init__.py
├── utils/
│   ├── report_generator.py    # PDF/Excel report generation
│   └── __init__.py
├── .env.example          # Environment variables template
└── README.md            # This file
```

### Adding New Features:

1. **New API Endpoints**: Add to `routes/api.py`
2. **Calculation Logic**: Extend `models/pension_calculator.py`
3. **Report Generation**: Modify `utils/report_generator.py`

## Production Deployment

For production deployment:

1. Use a production WSGI server (Gunicorn)
2. Set up a database (PostgreSQL recommended)
3. Configure proper logging
4. Set up monitoring and error tracking
5. Use environment variables for sensitive data

## License

This project is developed for HackYeah 2025 hackathon.
