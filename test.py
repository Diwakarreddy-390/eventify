from db_connecetion import get_connection

# Connect to database
conn = get_connection()
cursor = conn.cursor()

cursor.execute("""DROP TABLE events;
""")
cursor.close()
conn.close()