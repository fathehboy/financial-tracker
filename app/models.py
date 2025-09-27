# Data model & mapping for catatan-keuangan

TRANSACTION_MAPPING = {
    "mappings": {
        "properties": {
            "@timestamp": {"type": "date"},
            "category": {"type": "keyword"},
            "description": {"type": "text"},
            "nominal": {"type": "long"},
            "type": {"type": "keyword"}
        }
    }
}

class Transaction:
    def __init__(self, timestamp, category, description, nominal, type_):
        self.timestamp = timestamp
        self.category = category
        self.description = description
        self.nominal = nominal
        self.type = type_