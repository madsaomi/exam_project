import urllib.request
import urllib.parse
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import ContactMessage
import threading

TELEGRAM_BOT_TOKEN = '8856628938:AAETXOpqB56lfkWAPPEy-5OQpyDXFrlKGAU'
TELEGRAM_CHAT_ID = '8008022700'

def send_message_thread(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = urllib.parse.urlencode({'chat_id': TELEGRAM_CHAT_ID, 'text': text}).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req) as response:
            pass
    except Exception as e:
        print("Failed to send telegram message:", e)

@receiver(post_save, sender=ContactMessage)
def send_telegram_message(sender, instance, created, **kwargs):
    if created:
        text = f"📦 Yangi buyurtma/xabar!\n\n👤 Ism: {instance.name}\n📞 Tel: {instance.phone}\n✉️ Email: {instance.email}\n📝 Xabar:\n{instance.message}"
        # Run in a background thread to prevent blocking the HTTP response
        threading.Thread(target=send_message_thread, args=(text,)).start()
