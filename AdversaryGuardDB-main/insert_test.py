import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ids_project",
    user="postgres",
    password="shree2024"
)

cur = conn.cursor()

cur.execute("""
INSERT INTO query_logs
(query_text, query_count, risk_score, prediction)
VALUES
('SELECT * FROM users', 50, 20.5, 'Normal')
""")

conn.commit()

print("Record inserted successfully!")

cur.close()
conn.close()