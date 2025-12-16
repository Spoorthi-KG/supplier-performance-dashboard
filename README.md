# Supplier Performance Dashboard

**By:** SPOORTHI K.G
**Project:** TYA Internship Assessment  
**Date:** December 2024

---

## What This Project Does

This dashboard helps businesses monitor their suppliers by showing 5 key performance numbers:
- How often suppliers deliver on time
- How accurate their invoices are
- How many invoices get rejected
- Average payment time
- Average outstanding balances

Instead of checking spreadsheets manually, managers can see everything in one place with interactive charts.

---

## Why I Built This

Companies work with multiple suppliers and need to know who's reliable. Checking this manually takes hours. My dashboard automates this - just open the webpage, apply filters, and see results instantly.

---

## Technologies I Used

**Python** - Main programming language  
**Streamlit** - Creates the web dashboard (chose this because it's simpler than building with Flask)  
**Pandas** - Handles data calculations and filtering  
**Plotly** - Makes interactive charts that users can hover over and explore  
**SQLite** - Stores the data (lightweight, perfect for this project size)  
**Pytest** - Tests my calculations to ensure accuracy  
**Faker** - Generates realistic fake data for testing

---

## How to Run This

### What You Need
- Python 3.8 or newer
- Internet connection

### Setup Steps

**1. Get the code:**
```bash
git clone [YOUR-REPO-URL]
cd supplier-performance-dashboard
```

**2. Create virtual environment:**

Windows:
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install packages:**
```bash
pip install -r requirements.txt
```

**4. Generate sample data:**
```bash
python data_generator.py
```

This creates fake data: 20 suppliers, 500 invoices, 50 outstanding payments.

**5. Start dashboard:**
```bash
streamlit run app.py
```

Opens automatically in your browser at `http://localhost:8501`

---

## Using the Dashboard

**Main Screen:**
- Top section shows 5 KPI numbers
- Left sidebar has filters (supplier, date range, category)
- Middle section shows data table
- Bottom has tabs with different chart views

**Filters:**
- Select specific suppliers from dropdown
- Pick date ranges to analyze different periods
- Choose categories to focus on supplier types

**Charts:**
- **Performance Comparison:** Bar charts showing best/worst suppliers
- **Trends:** Line graph showing changes over time
- **Distribution:** Histograms and breakdowns
- **Drill-Down:** Detailed view of individual suppliers

**Export:**
- Click download buttons at bottom
- Get CSV files to use in Excel

---

## Project Structure

```
supplier-dashboard/
├── app.py                    # Main dashboard
├── data_generator.py         # Creates test data
├── database.py               # Database operations
├── kpi_calculator.py         # KPI calculations
├── tests/
│   └── test_kpis.py         # Unit tests
├── data/
│   ├── suppliers.db         # SQLite database
│   └── sample_export.csv    # Sample data
├── README.md
├── requirements.txt
└── .gitignore
```

---

## About the Sample Data

Since I don't have real company data, I generated realistic fake data:

**Suppliers:** 20 fake companies in 5 countries (USA, India, China, Germany, Japan)  
**Categories:** Raw Materials, Electronics, Packaging, Logistics  
**Invoices:** 500 records over 12 months, amounts $1,000-$50,000  
**Patterns:** Some suppliers consistently late, others reliable (realistic behavior)

---

## How I Calculate KPIs

**On-Time Delivery:**
```
(Deliveries on time ÷ Total deliveries) × 100
On-time means: actual delivery ≤ expected delivery date
```

**Invoice Accuracy:**
```
(Accurate invoices ÷ Total invoices) × 100
```

**Rejection Rate:**
```
(Rejected invoices ÷ Total invoices) × 100
```

**Average Payment Days:**
```
Sum of payment times ÷ Number of invoices
Payment time = payment date - invoice date
```

**Average Outstanding:**
```
Sum of unpaid amounts ÷ Number of records
```

---

## Testing

I wrote 12 unit tests to verify calculations are correct.

**Run tests:**
```bash
pytest tests/test_kpis.py -v
```

**What I test:**
- Each KPI calculation with sample data
- Edge cases (empty data, single record)
- Large datasets
- Accuracy of percentages and averages

All tests must pass before submission.

---

## Problems I Solved

**Date Filtering Issue:**  
Dates in SQLite are stored as text. My comparisons failed until I converted them properly using datetime.

**Empty Charts:**  
Plotly needs specific date format. I was passing the wrong type, fixed by converting Period to Timestamp.

**Git Upload Size:**  
First push failed because it tried uploading venv folder (huge). Created .gitignore to exclude it.

**Virtual Environment Activation:**  
PowerShell blocked scripts. Switched to Command Prompt where activate.bat works without issues.

---

## What I Learned

**Technical Skills:**
- Building web dashboards with Streamlit
- Complex data filtering with Pandas
- Creating interactive visualizations
- Writing effective unit tests
- SQL queries with parameters

**Problem Solving:**
- Reading error messages carefully
- Breaking big problems into smaller tasks
- Testing each component separately
- Debugging systematically

**Best Practices:**
- Modular code organization
- Virtual environments for projects
- Version control with Git
- Documentation importance

---

## Future Improvements

If I continue this project:
- Add email alerts when KPIs drop below thresholds
- Connect to real ERP systems instead of sample data
- Add user login and role-based access
- Implement ML to predict supplier risk
- Create PDF report export option
- Add comparison view (this month vs last month)

---

## Contact

**Email:** spoorthikg7@gmail.com 
**GitHub:**  https://github.com/Spoorthi-KG/supplier-performance-dashboard

---

## Acknowledgments

Thank you to TYA for this opportunity to build a practical data analytics project. Special thanks to the Streamlit and Pandas communities for excellent documentation.

---

**Project Status:** Completed   
**Last Updated:** December 2024

---

*Built with Python, dedication, and lots of coffee* 
