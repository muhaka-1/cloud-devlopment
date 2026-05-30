import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="student",
    password="student",
    database="shop"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM customers")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()
