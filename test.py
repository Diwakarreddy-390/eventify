from db_connecetion import get_connection

# Connect to database
conn = get_connection()
cursor = conn.cursor()
email = "mouni@gmail.com"
cursor.execute("""CREATE TABLE ticket_purchases (
    purchase_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    event_number INT,
    purchase_time TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (event_number) REFERENCES events(event_number)
);
""")


