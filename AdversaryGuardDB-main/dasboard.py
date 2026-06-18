import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# --------------------------
# DATABASE CONNECTION
# --------------------------

conn = psycopg2.connect(
    host="localhost",
    database="ids_project",
    user="postgres",
    password="shree2024"
)

# --------------------------
# LOAD DATA
# --------------------------

query_logs = pd.read_sql(
    "SELECT * FROM query_logs",
    conn
)

alerts = pd.read_sql(
    "SELECT * FROM security_alerts",
    conn
)

# --------------------------
# DASHBOARD TITLE
# --------------------------

st.title("🚨 Query Risk Detection Dashboard")

# --------------------------
# METRICS
# --------------------------

col1, col2, col3 = st.columns(3)

col1.metric("Total Queries", len(query_logs))
col2.metric("Total Alerts", len(alerts))
col3.metric("Normal Traffic", len(query_logs))

# --------------------------
# QUERY COUNT GRAPH
# --------------------------

st.subheader("Query Count Distribution")

fig1 = px.histogram(
    query_logs,
    x="query_count",
    title="Query Count"
)

st.plotly_chart(fig1)

# --------------------------
# RISK SCORE GRAPH
# --------------------------

st.subheader("Risk Score")

fig2 = px.line(
    query_logs,
    y="risk_score",
    title="Risk Score Trend"
)

st.plotly_chart(fig2)

# --------------------------
# ALERTS TABLE
# --------------------------

st.subheader("Security Alerts")

st.dataframe(alerts)

# --------------------------
# QUERY LOGS TABLE
# --------------------------

st.subheader("Query Logs")

st.dataframe(query_logs)

# --------------------------
# CLOSE CONNECTION
# --------------------------

conn.close()