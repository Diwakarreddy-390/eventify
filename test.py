import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv("server.env")

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
conn = get_connection()
cursor = conn.cursor()
cursor.execute("""CREATE TABLE ticket_purchases (
    purchase_id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    event_number INT NOT NULL,
    purchase_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (purchase_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (event_number) REFERENCES events(event_number)
);
""")
