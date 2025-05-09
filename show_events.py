from db_connecetion import get_connection
import base64

def show(location):
    try:
        # Open a new connection and cursor each time the function is called
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT title, description, date_time, location, photo, event_number FROM events WHERE location=%s", (location,))
        events = cursor.fetchall()

        event_list = []

        for row in events:
            if row[4]:
                photo_base64 = base64.b64encode(row[4]).decode('utf-8')
                photo_data = f"data:image/jpeg;base64,{photo_base64}"
            else:
                photo_data = None

            event_list.append({
                "title": row[0],
                "event_datetime": row[1],
                "description": row[2],
                "location": row[3],
                "photo": photo_data,
                "event_id": row[5],
                
            })
    except Exception as e:
        print(f"Database Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

    return event_list
