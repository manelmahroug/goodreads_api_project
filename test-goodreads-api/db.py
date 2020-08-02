import psycopg2
conn = psycopg2.connect(user="postgres", password="123", database="postgres", host="localhost", port="5432")
print("Successfully connected!")