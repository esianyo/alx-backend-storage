from pymongo import MongoClient

def nginx_logs_stats():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    status_logs = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_logs} status check")

nginx_logs_stats()
