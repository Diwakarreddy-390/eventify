from db_connecetion import get_connection
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
        cursor.execute("SELECT title, date_time, image, description,location FROM events WHERE created=%s", (self.email,))
        events = cursor.fetchall()
        event_list = [{"title": row[0], "event_datetime": row[1], "image_name": row[2], "description": row[3],"location":row[4]} for row in events]
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
    


    


