from db_connection import get_client


SENSITIVE_KEYWORDS = ["password", "token", "session", "otp", "secret", "key"]

def is_sensitive(field_name):
    lower = field_name.lower()
    return any(word in lower for word in SENSITIVE_KEYWORDS)

def inspect_collection(db, name):
    collection = db[name]
    count = collection.count_documents({})

  
    sample_docs = list(collection.find({}).limit(3))

    fields = set()
    for doc in sample_docs:
        fields.update(doc.keys())

    safe_fields = sorted([f for f in fields if not is_sensitive(f)])
    hidden_fields = sorted([f for f in fields if is_sensitive(f)])

    return {
        "name": name,
        "count": count,
        "fields": safe_fields,
        "hidden_sensitive_fields": hidden_fields
    }

def main():
    client = get_client()
    db = client["techtrax"]

    collection_names = sorted(db.list_collection_names())

    print(f"Found {len(collection_names)} collections in 'techtrax'\n")
    print("=" * 80)

    for name in collection_names:
        info = inspect_collection(db, name)
        print(f"\nCollection: {info['name']}")
        print(f"  Document count: {info['count']}")
        print(f"  Fields: {info['fields']}")
        if info["hidden_sensitive_fields"]:
            print(f"  Hidden sensitive fields (excluded above): {info['hidden_sensitive_fields']}")

    print("\n" + "=" * 80)
    print("Inventory complete.")

if __name__ == "__main__":
    main()