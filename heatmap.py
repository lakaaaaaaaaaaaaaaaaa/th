import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- FIX: Get the correct file path for VS Code ---
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'AIML Dataset.csv')

try:
    df = pd.read_csv(file_path)
    print("✅ File loaded successfully!")
except FileNotFoundError:
    print(f"❌ Error: Could not find '{file_path}' in the folder.")
    exit()

def analyze_fraud_distribution(df):
    counts = df['isFraud'].value_counts()
    percent = df['isFraud'].value_counts(normalize=True) * 100

    print(f"Số lượng giao dịch: \n{counts}")
    print(f"Tỉ lệ phần trăm: \n{percent}")

    plt.figure(figsize=(6,4))
    # Note: Added 'hue' to avoid warning in newer seaborn versions
    sns.barplot(x=counts.index, y=counts.values, hue=counts.index, palette='viridis', legend=False)
    plt.title("Phân phối Giao dịch Gian lận (0: Sạch, 1: Gian lận)")
    plt.show()

def analyze_money_flow(df):
    fraud_df = df[df['isFraud'] == 1].copy() # Added .copy() to prevent warnings

    # Checking if column is 'oldbalanceOrg' or 'oldbalanceOrig'
    col = 'oldbalanceOrg' if 'oldbalanceOrg' in fraud_df.columns else 'oldbalanceOrig'

    fraud_df['diff_orig'] = fraud_df[col] - fraud_df['amount'] - fraud_df['newbalanceOrig']

    print("Thống kê chênh lệch số dư tại nguồn của giao dịch gian lận:")
    print(fraud_df['diff_orig'].describe())

    plt.figure(figsize=(10,6))
    plt.scatter(fraud_df[col], fraud_df['amount'], alpha=0.5, color='red')
    plt.plot([0, max(fraud_df[col])], [0, max(fraud_df[col])], color='blue', linestyle='--')
    plt.xlabel("Số dư gốc")
    plt.ylabel("Số tiền giao dịch")
    plt.title("Pattern: Gian lận thường rút sạch tiền trong tài khoản")
    plt.show()

def plot_correlation(df):
    corr = df.select_dtypes(include=['number']).corr()

    plt.figure(figsize=(12,10))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Ma trận tương quan giữa các đặc trưng")
    plt.show()

# Execution
print("--- ĐANG PHÂN TÍCH PHÂN PHỐI GIAN LẬN ---")
analyze_fraud_distribution(df)

print("\n--- ĐANG PHÂN TÍCH LUỒNG TIỀN ---")
analyze_money_flow(df)

print("\n--- ĐANG VẼ MA TRẬN TƯƠNG QUAN ---")
plot_correlation(df)