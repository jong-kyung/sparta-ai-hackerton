import smtplib
from email.mime.text import MIMEText
import os
import streamlit as st


os.environ["SENDER_EMAIL"] = st.secrets["SENDER_EMAIL"]
os.environ["SENDER_PASSWORD"] = st.secrets["SENDER_PASSWORD"]

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")

def send_alert_email(subject, body, email):
    receiver_email = email  

    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ 이메일 전송 실패: {e}")
        return False
