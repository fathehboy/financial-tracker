# Entry point for testing CRUD
from app.crud import create_transaction, get_transaction, update_transaction, delete_transaction

if __name__ == "__main__":
    # Example usage
    data = {
        "@timestamp": "2025-09-27T10:00:00",
        "category": "makan",
        "description": "Sarapan pagi",
        "nominal": 25000,
        "type": "expense"
    }
    doc_id = create_transaction(data)
    print("Created:", doc_id)
    print("Read:", get_transaction(doc_id))
    update_transaction(doc_id, {"description": "Sarapan + kopi"})
    print("Updated:", get_transaction(doc_id))
    delete_transaction(doc_id)
    print("Deleted.")
