import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="stopwatch",
    user="stopwatch",
    password="stopwatch123"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE,
    region VARCHAR(100),
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()

print("✅ users table created successfully!")

cur.close()
conn.close()
