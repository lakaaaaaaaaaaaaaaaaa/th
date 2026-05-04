import pandas as pd
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Update this to your actual filename
file_path = os.path.join(script_dir, 'AIML Dataset.csv') 

try:
    df_fraud = pd.read_csv(file_path)
    print("✅ File loaded successfully!")
except FileNotFoundError:
    print(f"❌ Error: Could not find '{file_path}'. Make sure the CSV is in the same folder as this script.")
    exit()

# 1. Check for balance discrepancies
# Note: Fixed 'oldbalanceOrg' vs 'oldbalanceOrig' consistency based on common dataset naming
orig_col = 'oldbalanceOrg' if 'oldbalanceOrg' in df_fraud.columns else 'oldbalanceOrig'

df_fraud['errorBalanceOrig'] = df_fraud['newbalanceOrig'] + df_fraud['amount'] - df_fraud[orig_col]
df_fraud['errorBalanceDest'] = df_fraud['oldbalanceDest'] + df_fraud['amount'] - df_fraud['newbalanceDest']

# 2. Filter for only suspicious types
relevant_types = ['TRANSFER', 'CASH_OUT']
df_clean = df_fraud[df_fraud['type'].isin(relevant_types)].copy()

# 3. Drop columns that are just unique IDs
df_clean = df_clean.drop(['nameOrig', 'nameDest'], axis=1)

print(f"Cleaned data shape: {df_clean.shape}")

def detect_pro_fraud(df):
    analysis_df = df.copy()
    
    # Using the detected column name from earlier
    col = 'oldbalanceOrg' if 'oldbalanceOrg' in analysis_df.columns else 'oldbalanceOrig'

    # Rule 1: The account is wiped to EXACTLY zero
    rule_wipeout = (analysis_df['newbalanceOrig'] == 0) & (analysis_df[col] > 0)

    # Rule 2: The destination account is a "Ghost"
    rule_ghost_dest = (analysis_df['oldbalanceDest'] == 0) & (analysis_df['newbalanceDest'] == 0)

    # Combine
    analysis_df['is_pro_suspicious'] = (
        analysis_df['type'].isin(['TRANSFER', 'CASH_OUT']) &
        rule_wipeout &
        rule_ghost_dest
    ).astype(int)

    return analysis_df

# Apply the tighter rules
df_refined = detect_pro_fraud(df_clean)

# Metrics Calculation
new_flags = df_refined['is_pro_suspicious'].sum()
final_hits = df_refined[(df_refined['is_pro_suspicious'] == 1) & (df_refined['isFraud'] == 1)].shape[0]
final_misses = df_refined[(df_refined['is_pro_suspicious'] == 1) & (df_refined['isFraud'] == 0)].shape[0]

# Prevent division by zero error
new_precision = (final_hits / (final_hits + final_misses)) * 100 if (final_hits + final_misses) > 0 else 0

print(f"Total Transactions Flagged (Tighter Rules): {new_flags}")
print(f"✅ Final Hits: {final_hits}")
print(f"❌ Final Misses: {final_misses}")
print(f"🎯 New Precision: {new_precision:.2f}%")

total_actual_fraud = df_fraud['isFraud'].sum()
print(f"Total Fraud cases in the entire dataset: {total_actual_fraud}")

actual_hits_in_flags = final_hits
recall = (actual_hits_in_flags / total_actual_fraud) * 100 if total_actual_fraud > 0 else 0

print(f"Out of {total_actual_fraud} actual frauds, we caught {actual_hits_in_flags}.")
print(f"Recall: {recall:.2f}%")