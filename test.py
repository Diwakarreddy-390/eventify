import os

app_password = os.getenv("EMAIL_APP_PASSWORD")

# Example: using it in SMTP login
print(app_password)
