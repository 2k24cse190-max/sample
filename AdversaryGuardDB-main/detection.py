def threshold_detection(df, avg_query_count, avg_query_length):
    print("\n--- Simple Threshold Detection ---")
    for i, row in df.iterrows():
        if row["query_count"] > avg_query_count * 2 or row["query_length"] > avg_query_length * 2:
            print(f"User {row['user']} -> Suspicious")
        else:
            print(f"User {row['user']} -> Normal")


def zscore_detection(df):
    print("\n--- Z-Score Detection ---")
    for i, row in df.iterrows():
        if abs(row["z_score"]) > 1.5:
            print(f"User {row['user']} -> Suspicious")
        else:
            print(f"User {row['user']} -> Normal")


def query_spike_detection(df, avg_length):
    print("\n--- Query Length Spike Detection ---")
    for i, row in df.iterrows():
        if row["query_length"] > avg_length * 1.8:
            print(f"User {row['user']} -> Long Query Detected")
