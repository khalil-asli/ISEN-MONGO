# -*- coding: utf-8 -*-
 

import sys
import requests
import json
from pymongo import *
from pymongo import MongoClient, DESCENDING
from pprint import pprint
import datetime
from bson.son import SON
    
#Business Program:

 

# 1) Find station with name (with some letters) :
    
def search_station_with_name(city,name_station):
    
    try:
        client = MongoClient("mongodb+srv://123456:khalil1234@cluster0.welnc.mongodb.net/test?retryWrites=true&w=majority")
        print("\n Connection done. Please be patient...\n")
    except:
           print("Please retry! Connection failed.")
    db = client.test       
    station_finded= db.vLille.find({"name": {"$regex" : name_station}})    
    for station in station_finded : 
        print(station)

 

# 2) Update a station using her ID :  
 
def update_a_stations(id_statToUpdate): 
    
    try:
        client = MongoClient("mongodb+srv://123456:khalil1234@cluster0.welnc.mongodb.net/test?retryWrites=true&w=majority")
        print("\n Connection done. Please be patient...\n")
    except:
        print("Please retry! Connection failed.")
    db = client.test   
    # Station information to update :
    name = input("Please enter the name : ")     
    bike_available=input("Please enter the Bike available : ")
    Stand_available=(input("Please enter the Stand available : "))
    cord=[float(input("Please enter the latitude : ")),float(input("Please enter the longitude : "))]
    date_info=str( input("Please enter the date : "))
    #Update infos
    db.updateddata.update_one({"_id":id_statToUpdate},
                {'$set': {
                "name": name,
                "bike_availbale":bike_available,
                "stand_availbale": Stand_available,
                "Cord": {'coordinates': cord, 'type': 'Point'},
                "date": date_info
           } })     
    print("\n\nThe station :",name,"has been successfully updated!")
         
# 3) Delete a station and datas : 
       
def delete_station_data(city, name_stat):
    
    try:
        client = MongoClient("mongodb+srv://123456:khalil1234@cluster0.welnc.mongodb.net/test?retryWrites=true&w=majority")
        print("\n Connection done. Please be patient...\n")
    except:
        print("Please retry! Connection failed.")
    db = client.test   
     # All cities :  
    all_city = {"lille" : db.vLille, "lyon" : db.test.vLyon, "rennes" : db.vRennes, "paris" :  db.vParis}
     # Choice of city in the list :
    choose_city = all_city[city]
    # Delete a station and datas
    deleted_stations = choose_city.delete_many({"name": {"$regex" : name_stat}})   
    print("\nThe station",name_stat,"in",city,"has been successfully deleted. Thanks")  
 

 

# 4) Deactivate all station in an area : 
 
def desactivate(ville):
    #Coordinate table:
    # 2 stations in the polygon 
    tab = [[[3.04876, 50.634272], [3.0530628, 50.6357694,], [3.066667, 50.633333], [3.051335, 50.62767], [3.04876, 50.634272]]]
    # 1 station in the polygon 
    tab2 = [[[3.04876, 50.634272], [3.0530628, 50.6357694,], [3.066667, 50.633333], [3.049479, 50.631634], [3.04876, 50.634272]]]   
    try:
        client = MongoClient("mongodb+srv://123456:khalil1234@cluster0.welnc.mongodb.net/test?retryWrites=true&w=majority")
        print("\n Connection done. Please be patient...\n")
    except:
        print("Please retry! Connection failed.")
    
    db = client.test
    
    #We created a dictionary of city collections then chose a city from the list:
    CollectionOfCities = {"lille" : db.vLille, "lyon" : db.test.vLyon, "rennes" : db.vRennes, "paris" :  db.vParis}
    Cities_Collection = CollectionOfCities[ville]
    
    # We create the index and we list the stations present in the polygon:
    Cities_Collection.create_index([("geometry", "2dsphere")])
    find_in_polygon = Cities_Collection.find({'geometry': {'$geoWithin': SON([('$geometry', SON([('type', 'Polygon'), ('coordinates', tab)]))])}}).sort("timestamp", -1)
    listOfstations_name = find_in_polygon.distinct("name")
    station = find_in_polygon[0]
    if(len(listOfstations_name) > 1) :
        print("The following stations  in the polygon have been deactivated:")
        i = 0
        for station_name in listOfstations_name : 
            print("\n")
            print(i , ' ) ' , station_name)
            i += 1
            #Deactivate the station
            Cities_Collection.update_many({"name" : station_name}, {"$set" : {"en service" : False}})
            #The most recent information is displayed
            station = Cities_Collection.find({"name": {"$regex" : station_name}}).sort("timestamp", -1)[0]
            print(station)
    else:
        Cities_Collection.update_many({"name" : listOfstations_name[0]}, {"$set" : {"en service" : False}})
        print("The station is in the polygon : ", listOfstations_name[0])
        print("The station have been deactived : \n" , station)
    
# 5) Give all stations with a ratio bike/total_stand under 20% between 18h and 19h00 (monday to friday) :   
def get_all_stations_with_a_ratio_bike_total():
    
    ListOfDays = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"] 
    client = MongoClient('mongodb+srv://123456:khalil1234@cluster0.welnc.mongodb.net/test?retryWrites=true&w=majority')
    db = client.test
    my_collection = db['updateddata']
    save = my_collection.find({})
    for elem in save:    
        getDate = (elem.get('date')).strftime("%A")
        getHour = (elem.get('date')).hour       
        ratio = 0
        if elem.get('stand_availbale') == 0:
            ratio = 100
        else:
            ratio = (elem.get('bike_availbale') / elem.get('stand_availbale'))*100            
        if getDate.upper() in ListOfDays:
            if 18 <= getHour <= 19:
                if ratio < 20:                    
                    print("Name Station : "+elem.get("name"))
                    print("Bike Available:", elem.get("bike_availbale"))
                    print("Stand Available :",elem.get("stand_availbale"))
                    print("Date and Hour: ",elem.get("date"))
                    print(" \n")

 

#Test Function : 
    
def __main__():

 

    choice=True
    while choice:
        
        print("\n Business program :\n ")
        print("1 : Find station with name (with some letters)\n")
        print("2 : Update a stations with ID of Station:\n") 
        print("3 : Delete a station and datas :\n") 
        print("4 : Deactivate all station in an area :\n") 
        print("5 : Give all stations with a ratio bike/total_stand under 20% between 18h and 19h00 (monday to friday) \n")  
        print("6 : Exit/Quit\n")
    
        choice=int(input("\n What would you like to do ? ")) 
        
        if choice==1: 
            letter=input("Please enter the letters you want to find a station : ")
            search_station_with_name("lille",letter)
            
        elif choice==2:
            IdOfStation=input("Please enter the ID of the station you want to update :")
            update_a_stations(IdOfStation)
            
        elif choice==3:
            StationName=input("Please enter the station name you want to delete : ")
            delete_station_data("lille",StationName) 
            
        elif choice==4:
            desactivate("lille")
            
        elif choice ==5: 
            get_all_stations_with_a_ratio_bike_total()
            
        elif choice ==6:  
            print ("\n The end of the Program.")
            sys.exit()
                          
        else:
            print("\n Not a Valid Choice Try again")
            __main__() 

 

__main__()    
