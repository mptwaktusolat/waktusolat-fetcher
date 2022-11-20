import json
import os
from pprint import pprint
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('adminsdk-creds.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

# Open *=*.processed.json file
y = os.listdir("outputs")

processed_file = [x for x in y if x.endswith(".processed.json")][0]

# extract month and year from filename
x = processed_file.split(".")[0]
month, year = x.split("-")

print(f"Want to push for {month} {year}")

month_ref = db.collection('waktusolat').document(f'{year}').collection(month)

with open(f'outputs/{processed_file}') as f:
    raw_data = json.load(f)

# iterate the zones
for zone in raw_data["processed"]:
    zone_name = zone["zone"]
    prayer_times = zone["prayerTime"]

    # push to firebase
    z = month_ref.document(zone_name).set({"prayerTime": prayer_times})
    print(":white_check_mark: Pushed", zone_name)
