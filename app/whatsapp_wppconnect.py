# WhatsApp integration using WPPConnect REST API
import os
import requests
from dotenv import load_dotenv

load_dotenv()

WPP_URL = os.getenv("WPP_URL", "http://localhost:21465")
WPP_SESSION = os.getenv("WPP_SESSION", "mySession")
WPP_TOKEN = os.getenv("WPP_TOKEN", "YOUR_BEARER_TOKEN")

def send_whatsapp_message(phone, message):
    url = f"{WPP_URL}/api/{WPP_SESSION}/send-message"
    payload = {
        "phone": phone,
        "message": message
    }
    headers = {
        "Authorization": f"Bearer {WPP_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print("Status code:", response.status_code)
    print("Raw response:", response.text)
    try:
        return response.json()
    except Exception:
        return None

# Example usage:
if __name__ == "__main__":
    result = send_whatsapp_message("6281326610168", "Halo dari Financial Tracker!")
    print(result)
