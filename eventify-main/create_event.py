from db_connecetion import get_connection

conn = get_connection()
cursor = conn.cursor()

def create(title,date,location,description,image,email):
    cursor.execute("""INSERT INTO events (title, date_time, location, description, image, created)
             VALUES (%s, %s, %s, %s, %s, %s)""",(title, date, location, description, image, email))
    conn.commit()
    cursor.close()
    conn.close()