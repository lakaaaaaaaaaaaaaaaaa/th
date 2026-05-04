import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- FIX: Get the correct file path ---
script_dir = os.path.dirname(os.path.abspath(__file__))
# Note: Ensure the file name matches exactly what you have on your computer
file_path = os.path.join(script_dir, 'default of credit card clients.xls')

try:
    # Use engine='xlrd' for .xls files
    df = pd.read_excel(file_path, header=1)
    print("✅ Excel file loaded successfully!")
except FileNotFoundError:
    print(f"❌ Error: Could not find '{file_path}'.")
    print("Make sure the .xls file is in the same folder as this script.")
    exit()
except Exception as e:
    print(f"❌ An error occurred: {e}")
    exit()

# 1. Identify "Bust-Out" Pattern
# High debt compared to limit + zero payments
df['debt_ratio'] = df['BILL_AMT1'] / df['LIMIT_BAL']
df['is_high_risk'] = (df['debt_ratio'] > 0.9) & (df['PAY_AMT1'] == 0)

# 2. Identify "Serial Defaulters"
# PAY_0 > 0 means late. If they are late for 3 consecutive months:
df['serial_late'] = (df['PAY_0'] > 0) & (df['PAY_2'] > 0) & (df['PAY_3'] > 0)

# 3. Summary of potential "Fraudulent" Defaults
potential_fraud = df[df['is_high_risk'] & df['serial_late']].copy()

print(f"\nTotal High Risk Accounts Found: {len(potential_fraud)}")

# Display the first few rows in the terminal
if not potential_fraud.empty:
    print("\n--- Potential Fraudulent Accounts (Top 5) ---")
    print(potential_fraud[['ID', 'LIMIT_BAL', 'BILL_AMT1', 'debt_ratio']].head())
else:
    print("\nNo accounts matched the 'Bust-Out' criteria.")

# 4. Correlation Analysis
# Ensuring the target column name matches the common UCI dataset header
target_col = 'default payment next month'
if target_col not in df.columns:
    # Sometimes Excel imports change spaces to underscores
    target_col = 'default_payment_next_month'

pay_columns = ['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6', target_col]

plt.figure(figsize=(10, 8))
sns.heatmap(df[pay_columns].corr(), annot=True, cmap='Reds')
plt.title("Correlation of Payment Delays to Final Default")
plt.show()