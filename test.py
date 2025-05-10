from db_connecetion import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""CREATE TABLE ticket_purchases (
    purchase_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    event_number INT,
    purchase_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""")
