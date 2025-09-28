# Flask webhook untuk menerima pesan WhatsApp dan simpan ke Elasticsearch
from flask import Flask, request
from crud import create_transaction
from datetime import datetime

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    data = request.json
    msg = data.get('body', '')
    sender = data.get('from', '')
    timestamp = data.get('timestamp', None)
    # Format pesan: kategori|nominal|deskripsi
    try:
        category, nominal, description = msg.split('|')
        transaction = {
            "@timestamp": datetime.utcfromtimestamp(timestamp).isoformat() if timestamp else datetime.utcnow().isoformat(),
            "category": category,
            "description": description,
            "nominal": int(nominal),
            "type": "expense",
            "sender": sender
        }
        doc_id = create_transaction(transaction)
        return {"status": "success", "id": doc_id}
    except Exception as e:
        return {"status": "error", "msg": str(e)}, 400

if __name__ == "__main__":
    app.run(port=5000)
