import os
import smtplib
import requests
from email.mime.text import MIMEText
from dotenv import load_dotenv

def make_mail_content(renting_item):
    price = f"💶 Prijs: {renting_item.get('price', 'onbekend')} {renting_item.get('price_postfix', '')}"
    oppervlakte = f"📐 Oppervlakte: {renting_item.get('surface_area', '')}"
    date = f"Datum: {renting_item.get('date', 'onbekend')}"
    subject = f"{price} {oppervlakte} {date}"

    body = f"""
    🏠 {renting_item['title']}
    📍 Locatie: {renting_item.get('location', 'onbekend')}
    🛏️ Kamers: {renting_item.get('number_of_rooms', '')}
    🏷️ Interieur: {renting_item.get('interior', '')}
    🔗 Link: {renting_item['url']}
        """.strip()

    return subject, body

def send_email(item, sender, recipient, smtp_host, smtp_port, smtp_user, smtp_password):
    """Send a simple text email with listing info."""
    subject, body = make_mail_content(item)
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print(f"✅ Email sent: {item['url']}")
    except Exception as e:
        print(f"❌ Email failed for {item['url']}: {e}")

def send_mails(scraped_items, old_json):
    # Load environment variables from .env file
    load_dotenv()
    EMAIL_SECRET = os.getenv("EMAIL_SECRET")
    email_config = {
        'sender': 'lexmeulenkamp@gmail.com',
        'recipient': 'lexmeulenkamp@hotmail.nl',
        'smtp_host': 'smtp.gmail.com',
        'smtp_port': 587,
        'smtp_user': 'lexmeulenkamp@gmail.com',
        'smtp_password': EMAIL_SECRET
    }
    for json_item in scraped_items:
        url_key = list(json_item.keys())[0]
        item_info = json_item[url_key]  # The value dictionary
        if url_key not in old_json:
            send_email(item_info, **email_config)
            item_info["email_sent"] = True
            old_json[url_key] = item_info
        else:
            print(f"Already sent email with url\n {url_key}\n")

def make_telegram_message(renting_item):
    price = f"💶 Prijs: {renting_item.get('price', 'onbekend')} {renting_item.get('price_postfix', '')}"
    oppervlakte = f"📐 Oppervlakte: {renting_item.get('surface_area', '')}"
    date = f"Datum: {renting_item.get('date', 'onbekend')}"
    url = f"{renting_item.get('url', 'onbekend')}"
    message = f"{price} {oppervlakte} {date} \n {url}"

    return message

def send_telegram(scraped_item, CHAT_ID, PRIVATE_KEY):
    url = f"https://api.telegram.org/{PRIVATE_KEY}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": make_telegram_message(scraped_item)
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def send_telegram_notifications(scraped_items, old_json, always_send=False):
    # Load environment variables from .env file
    load_dotenv()
    # Access the API key and private key from environment variables
    CHAT_ID = os.getenv("CHAT_ID")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    for json_item in scraped_items:
        url_key = list(json_item.keys())[0]
        item_info = json_item[url_key]
        date = item_info["date"] # TODO based on time not email_sent
        if url_key not in old_json or always_send:
            send_telegram(item_info, CHAT_ID, PRIVATE_KEY)
            item_info["email_sent"] = True
            old_json[url_key] = item_info
        else:
            print(f"Already sent email with url\n {url_key}\n")
