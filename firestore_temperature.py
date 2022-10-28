import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

# Use a service account.
cred = credentials.Certificate("env/private_key.json")

try:
    app = firebase_admin.initialize_app(cred)
except ValueError:
    pass

db = firestore.client()
temp_ref = db.collection("bme_sensor")


def add_temperature_reading(data):
    temp_ref.add(data)


def read_from(from_timestamp):
    query_ref = (
        temp_ref.where("timestamp", ">=", from_timestamp)
        .order_by("timestamp", direction=firestore.Query.DESCENDING)
        .limit(432)  # 72h*6 (one reading every 10 minutes)
    )
    return [doc for doc in query_ref.stream()]


if __name__ == "__main__":
    data = {
        "humidity": 58.09,
        "pressure": 962.76,
        "temperature": 16.03,
        "timestamp": datetime.datetime(
            2022, 10, 28, 10, 0, 0, 914000, tzinfo=datetime.timezone.utc
        ),
    }
    add_temperature_reading(data)
