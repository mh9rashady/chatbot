from telethon import TelegramClient, events
import requests
import json
import urllib3

# غیرفعال کردن هشدارهای SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_id = 23794610
api_hash = '5fb4e6b65d161b9dc2559bdbd0cf8301'
phone = '+989166569607'

# آدرس Webhook که در n8n ساختی:
WEBHOOK_URL = 'https://eager-hodgkin-hfdx6x3khu.liara.run/webhook-test/2169b21f-40eb-4395-bf55-e4b2d64d01fd'

client = TelegramClient('my_session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handle_private_message(event):
    sender = await event.get_sender()
    chat = await event.get_chat()
    
    # فقط پی‌وی
    if event.is_private:
        text = event.raw_text
        user_id = sender.id
        username = sender.username or ""
        print(f"📩 پیام از {username} ({user_id}): {text}")

        # ارسال پیام به n8n
        data = {
            "user_id": user_id,
            "username": username,
            "text": text,
            "message_id": event.message.id
        }

        try:
            # اضافه کردن تنظیمات SSL و timeout
            response = requests.post(
                WEBHOOK_URL, 
                json=data, 
                verify=False,  # غیرفعال کردن بررسی SSL
                timeout=10,    # timeout 10 ثانیه
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"✅ ارسال موفق به n8n - status: {response.status_code}")
            else:
                print(f"⚠️ ارسال شد اما status code: {response.status_code}")
                
        except requests.exceptions.SSLError as e:
            print(f"❌ خطای SSL در ارسال به n8n: {e}")
        except requests.exceptions.Timeout as e:
            print(f"⏰ timeout در ارسال به n8n: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"🔌 خطای اتصال به n8n: {e}")
        except Exception as e:
            print(f"❌ خطای عمومی در ارسال به n8n: {e}")

client.start(phone=phone)
client.run_until_disconnected()
