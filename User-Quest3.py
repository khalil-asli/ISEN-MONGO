from pymongo import *
from pymongo import MongoClient, DESCENDING
from pprint import pprint
from bson.son import SON

 


client = MongoClient("mongodb+srv://123456:khalil1234@cluster0.welnc.mongodb.net/test?retryWrites=true&w=majority")
db = client.test
# Input of user lng and lat :
user_lng = float(input("Your lng(longitude) please :"))
user_lat = float(input("Your lat(latitude) please : "))
db.vLille.ensure_index([("geometry", GEOSPHERE)])
query =  db.vLille.find({"geometry" : SON([("$near", { "$geometry" : SON([("type", "Point"), ("coordinates", [user_lng, user_lat])])})])}).sort("record_timestamp",DESCENDING)
for i in query:
  print(i)
