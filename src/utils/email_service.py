import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(override=True)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = os.getenv("EMAIL")  
FROM_PASSWORD = os.getenv("EMAIL_PASSWORD")

BASE_URL = os.getenv("BACKEND_URL") 

def send_verification_email(to_email, token):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Verify your EchoPersona Account"
        msg["From"] = "EchoPersona <echopersona.noreplay@gmail.com>"
        msg["To"] = to_email

        verification_link = f"{BASE_URL}/verify-email/{token}"
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px;">
                <h2 style="color: #333;">Welcome to <span style="color:#6366f1;">EchoPersona</span>!</h2>
                <p>Thank you for registering. Please verify your email address by clicking the button below:</p>
                <a href="{verification_link}" style="display: inline-block; padding: 10px 20px; margin-top: 20px; background-color: #6366f1; color: white; text-decoration: none; border-radius: 5px;">Verify Email</a>
                <p style="margin-top: 30px; font-size: 12px; color: #888;">If you didn't create an account, you can safely ignore this email.</p>
                <p style="font-size: 12px; color: #888;">&copy; {datetime.now().year} EchoPersona. All rights reserved.</p>
            </div>
        </body>
        </html>
        """

        part = MIMEText(html, "html")
        msg.attach(part)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, FROM_PASSWORD)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        server.quit()

        print(f"Verification email sent to {to_email}")

    except Exception as e:
        print(f"Failed to send email: {e}")
