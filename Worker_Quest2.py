# Worker who refresh and store live data for a city (history data)
# Choose lille data

 

import requests
import json
from pprint import pprint
from pymongo import MongoClient

 

client = MongoClient('mongodb://localhost:27017/')
db = client.vls 
collection_vlilles = db.vlilles 

 

def get_velib(url):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

 


vlilles = get_velib("https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1")

 


vlilles_format = []
for vlib in vlilles:
    vlilles_format.append({
        "name": vlib["fields"]["nom"],
        "vlilles_dispo": vlib["fields"]["nbvelosdispo"],
        "places_dispo" : vlib["fields"]["nbplacesdispo"],
        "status": vlib["fields"]["etat"] == "EN SERVICE",
        "record_timestamp": vlib["record_timestamp"] })

 


print("inserted : " + str(len(collection_vlilles.insert_many(vlilles_format).inserted_ids)))
