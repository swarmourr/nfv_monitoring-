# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 15:30:50 2020


db for LAAS project 

@author: PARA
"""
import tinydb
from tinydb import TinyDB
from datetime import datetime
import atexit

def init():
    dbs =  ["monitoring", "Data","Symptomes"]
    for db  in dbs:
        if TinyDB(db+'.json'):
            print(TinyDB(db+'.json'))
            pass
        else:
           print("not exsit")
           print(TinyDB(db+'.json'))
           TinyDB(db+'.json')
    
def connect_database(name): 
    db = TinyDB(name+'.json')
    return db

def insert_data(db:tinydb.database.TinyDB ,data):
    if type(data) is dict:
        data["timestamp"]=datetime.timestamp(datetime.now())
        db.insert(data)
    elif type(data) is list:
        for agentData in data:
            agentData["timestamp"]=datetime.timestamp(datetime.now())
            db.insert(agentData)

def get_symptome(db:tinydb.database.TinyDB):
    return "agent"
        

#defining function to run on shutdown
@atexit.register
def close_running_threads():
    print("Threads complete, ready to finish")
#Register the function to be called on exit
        

#atexit.register(close_running_threads)