from db_connecetion import get_connection

def show(location):
    try:
        # Open a new connection and cursor each time the function is called
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT title, description, date_time, image,event_number FROM events WHERE location=%s", (location,))
        events = cursor.fetchall()
        
        event_list = []
        for event in events:
            event_dict = {
                "title": event[0],
                "description": event[1],
                "date_time": event[2],
                "image": event[3],
                "id":event[4]
            }
            event_list.append(event_dict)

    except Exception as e:
        print(f"Database Error: {e}")
        return []

    finally:
        cursor.close()
        conn.close()

    return event_list