import pandas as pd
import psycopg2

from features import compute_basic_stats, add_z_score
from detection import threshold_detection, zscore_detection, query_spike_detection
from risk_score import calculate_risk, classify
from ml_model import train_and_save_model, load_and_predict

# -------------------
# LOAD DATA
# -------------------
df = pd.read_csv("data.csv")

# -------------------
# FEATURES
# -------------------
avg_query_count, avg_query_length = compute_basic_stats(df)
df = add_z_score(df, avg_query_count)

print("Average Query Count:", avg_query_count)
print("Average Query Length:", avg_query_length)

# -------------------
# RULE-BASED DETECTION
# -------------------
threshold_detection(df, avg_query_count, avg_query_length)
zscore_detection(df)
query_spike_detection(df, avg_query_length)

# -------------------
# RISK SCORING
# -------------------
df = calculate_risk(df, avg_query_count, avg_query_length)
classify(df)

# -------------------
# ML TRAINING
# -------------------
print("\n--- Training ML Model ---")
model = train_and_save_model(df)

# -------------------
# ML PREDICTION
# -------------------
print("\n--- ML Predictions ---")
df = load_and_predict(df)

# -------------------
# INSERT INTO POSTGRESQL
#---------------------
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ids_project",
    user="postgres",
    password="shree2024"
)

cur = conn.cursor()

for i in range(len(df)):
    if df.iloc[i]["ml_prediction"] == 1:
        cur.execute("""
            INSERT INTO security_alerts (user_name, risk_score, prediction)
            VALUES (%s, %s, %s)
        """, (
            df.iloc[i]["user"],
            float(df.iloc[i]["risk_score"]),
            1
        ))
    else:
        cur.execute("""
            INSERT INTO query_logs (user_name, prediction, risk_score)
            VALUES (%s, %s, %s)
        """, (
            df.iloc[i]["user"],
            "NORMAL",
            float(df.iloc[i]["risk_score"])
        ))

conn.commit()
cur.close()
conn.close()

print("DB INSERT DONE")