import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="stopwatch",
        user="stopwatch",
        password="stopwatch123"
    )

    print("✅ Connected to PostgreSQL successfully!")

    conn.close()

except Exception as e:
    print("❌ Connection failed:")
    print(e)
