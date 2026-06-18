import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="ids_project",
        user="postgres",
        password="shree2024"
    )

    print("Connected Successfully!")

    conn.close()

except Exception as e:
    print("Error:", e)
    #this is sample commite