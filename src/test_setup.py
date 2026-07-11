from db_connection import get_client

client = get_client()
db = client["techtrax"]

data = list(db["crmconfigs"].find({}, {"_id": 0}))
print(f"Found {len(data)} documents")
print(data)