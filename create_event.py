from db_connecetion import get_connection

conn = get_connection()
cursor = conn.cursor()

def create(title,date,location,description,image,email):
    sql = """INSERT INTO events (title, date_time, location, description, image, email)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute("""INSERT INTO events (title, date_time, location, description, image, email)
             VALUES (%s, %s, %s, %s, %s, %s)""",(title, date, location, description, image, email))
    conn.commit()
    cursor.close()
    conn.close()