from db_connecetion import get_connection
import base64
from PIL import Image
from io import BytesIO
class Login:
    def __init__(self,email):
        self.email = email
    def check_user(self,password):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_type FROM users WHERE email=%s AND password=%s", (self.email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user[0] if user else None

    def admin_events(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT title, date_time, description, location, photo, image FROM events WHERE created=%s", (self.email,))
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
                "image_name": row[5]
            })

        cursor.close()
        conn.close()

        return event_list



    
    def event_count(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("select count(*) from events where created=%s", (self.email,))
        events = cursor.fetchone()
        cursor.close()
        conn.close()
        return events[0] if events else 0
    
    def name(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Full_name from users WHERE email=%s", (self.email,))
        name = cursor.fetchone()
        return name
    
    def explore(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT title, date_time, description, location, photo, image FROM events")
            events = cursor.fetchall()
            event_list = []

            for event in events:
                photo_data = None
                if event[4]:
                    photo_base64 = base64.b64encode(event[4]).decode('utf-8')
                    photo_data = f"data:image/jpeg;base64,{photo_base64}"

                event_list.append({
                    "title": event[0],
                    "event_datetime": event[1],
                    "description": event[2],
                    "location": event[3],
                    "photo": photo_data,
                    "image": event[5]
                })
            return event_list
        finally:
            cursor.close()
            conn.close()

            


            


