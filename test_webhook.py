import requests
import json

# آدرس Webhook از n8n
WEBHOOK_URL = 'https://eager-hodgkin-hfdx6x3khu.liara.run/webhook-test/2169b21f-40eb-4395-bf55-e4b2d64d01fd'

# داده تست
test_data = {
    "user_id": 123456789,
    "username": "test_user",
    "text": "این یک پیام تست است",
    "message_id": 1
}

print("🧪 تست اتصال به n8n webhook...")
print(f"📡 URL: {WEBHOOK_URL}")

try:
    response = requests.post(
        WEBHOOK_URL,
        json=test_data,
        verify=False,
        timeout=10,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"📊 Status Code: {response.status_code}")
    print(f"📄 Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ اتصال موفق!")
    else:
        print(f"⚠️ اتصال شد اما status code: {response.status_code}")
        
except Exception as e:
    print(f"❌ خطا: {e}")
