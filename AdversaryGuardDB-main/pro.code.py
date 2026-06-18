import pandas as pd
from features import compute_basic_stats, add_z_score
from detection import threshold_detection, zscore_detection, query_spike_detection
from risk_score import calculate_risk, classify
from ml_model import train_and_save_model, load_and_predict

# Load data
df = pd.read_csv("data.csv")

# Features
avg_query_count, avg_query_length = compute_basic_stats(df)
df = add_z_score(df, avg_query_count)

print("Average Query Count:", avg_query_count)
print("Average Query Length:", avg_query_length)

# Detection
threshold_detection(df, avg_query_count, avg_query_length)
zscore_detection(df)
query_spike_detection(df, avg_query_length)

# Risk scoring
df = calculate_risk(df, avg_query_count, avg_query_length)
classify(df)

# ML MODEL TRAINING

print("\n--- Training ML Model ---")
model = train_and_save_model(df)

# ML PREDICTION

print("\n--- ML Predictions ---")

df = load_and_predict(df)

for i, row in df.iterrows():
    if row["ml_prediction"] == 1:
        print(f"User {row['user']} -> ML DETECTED ATTACK")
    else:
        print(f"User {row['user']} -> ML NORMAL")
