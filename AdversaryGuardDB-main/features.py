import pandas as pd

def compute_basic_stats(df):
    avg_query_count = df["query_count"].mean()
    avg_query_length = df["query_length"].mean()
    return avg_query_count, avg_query_length

def add_z_score(df, avg_query_count):
    df["z_score"] = (df["query_count"] - avg_query_count) / df["query_count"].std()
    return df