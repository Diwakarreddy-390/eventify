import mysql.connector
from dotenv import load_dotenv
import os
import base64
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv("sql.env")

# Function to establish connection
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Connect to database
conn = get_connection()
cursor = conn.cursor()

# Fetch image data
email = "raju@gmail.com"
cursor.execute("SELECT photo FROM events WHERE created=%s", (email,))
img = cursor.fetchone()

if img:
    image_bytes = img[0]  # Extract binary image data
    image = Image.open(BytesIO(image_bytes))

    # Show image
    image.show()


# Close connections
cursor.close()
conn.close()