# save as: verify_files.py
import os, pandas as pd

master = 'data/PBJ_Daily_Nurse_Staffing_Q2_2024.csv'
supporting_dir = 'data/supporting/'

# Check master file
if os.path.exists(master):
    df = pd.read_csv(master, nrows=5)
    print(f'✅ Master CSV loaded — columns: {list(df.columns)}')
else:
    print('❌ Master CSV not found!')

# Check supporting files
files = os.listdir(supporting_dir)
print(f'\n📁 Supporting files found: {len(files)}')
for f in files:
    print(f'   {f}')
