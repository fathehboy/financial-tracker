# CRUD operations for catatan-keuangan
from .es_client import es
from .redis_client import redis_client
from .models import Transaction
from .utils import generate_uuid

INDEX_NAME = "financial-tracker"

# Create
def create_transaction(data):
    doc_id = generate_uuid()
    es.index(index=INDEX_NAME, id=doc_id, document=data)
    redis_client.set(doc_id, str(data))
    return doc_id

# Read
def get_transaction(doc_id):
    cached = redis_client.get(doc_id)
    if cached:
        return cached
    res = es.get(index=INDEX_NAME, id=doc_id)
    return res["_source"]

# Update
def update_transaction(doc_id, data):
    es.update(index=INDEX_NAME, id=doc_id, doc={"doc": data})
    redis_client.set(doc_id, str(data))

# Delete
def delete_transaction(doc_id):
    es.delete(index=INDEX_NAME, id=doc_id)
    redis_client.delete(doc_id)
