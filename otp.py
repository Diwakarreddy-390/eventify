import smtplib
from email.message import EmailMessage
import os  # Import to access environment variables

def send_otp_to_email(email, otp):
    """Function to send OTP via email"""
    msg = EmailMessage()
    msg.set_content(f"""Your OTP for eventify website created by Diwakar reddy  
                    OTP = {otp}""")
    msg["Subject"] = "OTP Verification"
    msg["From"] = "d8349934@gmail.com"
    msg["To"] = email

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "d8349934@gmail.com"
    app_password = os.getenv("EMAIL_APP_PASSWORD")  # Fetch App Password

    if not app_password:
        print("❌ Error: App Password not set.")
        return False

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
            print("✅ OTP email successfully sent!")
            return True  # 🔹 Make sure this happens after successful email sending
    except Exception as e:
        print(f"❌ Error sending OTP: {e}")
        return False
# Set the environment variable before running the script:
# export EMAIL_APP_PASSWORD="your_generated_app_password"