def calculate_risk(df, avg_query_count, avg_query_length):
    df["risk_score"] = 0

    for i, row in df.iterrows():
        score = 0

        if abs(row["z_score"]) > 1.5:
            score += 2
        if row["query_length"] > avg_query_length * 1.8:
            score += 2
        if row["query_count"] > avg_query_count * 2:
            score += 2

        df.at[i, "risk_score"] = score

    return df


def classify(df):
    print("\n--- Final Risk Score ---")
    for i, row in df.iterrows():
        if row["risk_score"] >= 4:
            print(f"User {row['user']} -> HIGH RISK")
        elif row["risk_score"] >= 2:
            print(f"User {row['user']} -> MEDIUM RISK")
        else:
            print(f"User {row['user']} -> LOW RISK")
