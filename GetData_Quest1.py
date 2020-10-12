import json
import requests
from pymongo import MongoClient
from pprint import pprint


def get_datalib(url):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

def get_dataVlyon(url):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("values", [])

vlille = get_datalib(
    "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1")
vLyon = get_dataVlyon(
    "https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json")
vParis = get_datalib(
    "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=-1")
vRennes = get_datalib(
    "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=stations_vls&q=&lang=fr&rows=-1")

format_vLille = []
for vlib in vlille:
    format_vLille.append({
        "name": vlib["fields"]["nom"],
        "city": vlib["fields"]["commune"],
        "size": vlib["fields"]["nbvelosdispo"] + vlib["fields"]["nbplacesdispo"],
        "geo": vlib["geometry"],
        "TPE ": vlib["fields"]["type"] != "SANS TPE",
        "status": vlib["fields"]["etat"] == "EN SERVICE",
        "last update": vlib["record_timestamp"] })


format_vRennes = []
for vlib in vRennes:
    format_vRennes.append({
        "name": vlib["fields"]["nom"],
        "city": "Rennes",
        "size": vlib["fields"]["nb_socles"],
        "geo": vlib["geometry"],
        "TPE ": vlib["fields"]["tpe"] == "oui",
        "status": vlib["fields"]["etat"] == 'Ouverte',
        "last update": vlib["record_timestamp"] })

format_vParis = []
for vlib in vParis:
    format_vParis.append({
        "name": vlib["fields"]["name"],
        "city": vlib["fields"]["nom_arrondissement_communes"],
        "size": vlib["fields"]["capacity"],
        "geo": vlib["geometry"],
        "TPE ": False,
        "status": vlib["fields"]["is_renting"] == 'OUI' and vlib["fields"]["is_returning"] == 'OUI',
        "last update": vlib["record_timestamp"] })

format_vLyon = []
for vlib in vLyon:
    format_vLyon.append({
        "name": vlib["name"],
        "city": vlib["commune"],
        "size": vlib["bike_stands"],
        "geo": {"type": "Point", "coordinates": [vlib["lng"], vlib["lat"]]},
        "TPE ": vlib["banking"],
        "status": vlib["status"] == "OPEN",
        "last update": vlib["last_update"] })


# AFFICHAGE
print("Lille : " + str(len(format_vLille)))
print("Lyon : " + str(len(format_vLyon)))
print("Rennes : " + str(len(format_vRennes)))
print("Paris : " + str(len(format_vParis)))

client = MongoClient('mongodb://localhost:27017/')
db = client.vls
collection = db.stations

#AFFICHAGE
print("inserted : " + str(len(collection.insert_many(format_vParis).inserted_ids)))
print("inserted : " + str(len(collection.insert_many(format_vLyon).inserted_ids)))
print("inserted : " + str(len(collection.insert_many(format_vRennes).inserted_ids)))
print("inserted : " + str(len(collection.insert_many(format_vLille).inserted_ids)))
