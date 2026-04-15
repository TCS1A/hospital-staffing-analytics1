# Hospital Staffing Analytics Project

## Overview
End-to-end data engineering pipeline built on CMS Payroll-Based
Journal (PBJ) Q2 2024 data — 14,564 US nursing facilities,
1.3 million daily staffing records.

## How to Run
pip3 install pandas numpy matplotlib streamlit plotly boto3

python3 verify_files.py       # Step 1 - verify files
python3 eda.py                # Step 2 - data analysis
python3 metrics.py            # Step 5 - calculate metrics
streamlit run dashboard.py    # Step 6 - launch dashboard

## Tech Stack & Why
- Python/Pandas: Industry standard for data manipulation
- AWS S3: Scalable, low-cost cloud storage
- AWS Glue: Serverless ETL, no servers to manage
- Streamlit: Fastest way to build dashboards in Python
- Plotly: Interactive charts with no frontend code needed

## Key Findings
1. Alaska leads nurse-to-patient ratio at 6.06 vs 3.37 national avg
2. California leads total nursing hours at 35.7 million for Q2
3. 92.3% of hours are direct employees, only 7.7% contractors
4. Three facilities reported zero nursing hours with 100+ patients
5. Patient census stable at 83.3-83.5 per facility across Q2 2024

## Questions Answered
1. Staffing vs occupancy: Census stable but ratios vary by state
   driven by regulations not patient volume
2. Highest overtime: Not calculatable - not in this dataset
3. Avg staffing by state: AK(6.06) PR(4.58) DC(4.54) lead in ratio
4. Length of stay: Not available in this dataset
