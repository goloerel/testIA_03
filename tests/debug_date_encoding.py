from datetime import date
from pymongo import MongoClient
import traceback

def reproduce():
    try:
        data = {
            "some_field": "value",
            "date_field": date(2027, 1, 29)
        }
        # Attempt to encode/insert into mongo (just checking bson encoding)
        from bson import BSON
        print("Attempting to encode data with datetime.date...")
        encoded = BSON.encode(data)
        print("Success!")
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    reproduce()
