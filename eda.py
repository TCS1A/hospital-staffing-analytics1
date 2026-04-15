import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load master file
df = pd.read_csv('data/PBJ_Daily_Nurse_Staffing_Q2_2024.csv', encoding='latin-1')

# Basic shape
print('Shape:', df.shape)
print('\nColumn types:')
print(df.dtypes)
print('\nFirst 5 rows:')
print(df.head())

# Missing values
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
print('\nMissing values (%):')
print(missing_pct[missing_pct > 0])

# Duplicates
print(f'\nDuplicate rows: {df.duplicated().sum()}')

# Basic stats
print('\nDescriptive statistics:')
print(df.describe())

# Total nurse hours column
df['total_nurse_hrs'] = df['Hrs_RN'] + df['Hrs_LPN'] + df['Hrs_CNA']

# Top 10 states by RN hours
state_hours = df.groupby('STATE')['Hrs_RN'].sum().sort_values(ascending=False)
print('\nTop 10 states by RN hours:')
print(state_hours.head(10))

# Missing values chart
if missing_pct[missing_pct > 0].empty:
    print('\n✅ No missing values found — skipping chart.')
else:
    missing_pct[missing_pct > 0].plot(kind='bar', figsize=(12, 5), color='steelblue')
    plt.title('Missing Values by Column (%)')
    plt.xlabel('Column')
    plt.ylabel('% Missing')
    plt.tight_layout()
    plt.savefig('outputs/missing_values.png')
    print('\nChart saved!')