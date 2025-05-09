from db_connecetion import get_connection

def create(title, date, location, description, image_filename, image_data, email):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""INSERT INTO events (title, date_time, location, description, image, photo, created)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                       (title, date, location, description, image_filename, image_data, email))
        conn.commit()
    except Exception as e:
        print(f"Error inserting event: {e}")
    finally:
        cursor.close()
        conn.close()