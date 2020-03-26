from  jvm_agents import  *
import ConfigParser
import requests
import urllib2
import json
import pprint
import os

config = ConfigParser.ConfigParser()
config.read(str(os.getcwd())+"/agent/api/builder/agent/config.conf")
alert={"type":"Alert"}
all_data=[]
stats={}
stat={"JVM":{}}
result={}


def info_jvm():
    global stats
    stats=info_m()

def mem_stat():
     for k in stats:
         tmp=k["Pid"]
         if  (float(k["MEM"])!=0.0 or float(k["CPU"])!=0.0 ):
             if  ((tmp  in  stat["JVM"].keys())):
                  if "RAM" in stat["JVM"][tmp]:
                      pass
                  else :
                      stat["JVM"][tmp]["RAM"]=[]
             else :
                 #stat["JVM"][tmp]={"RAM":[],"CPU":[]}
                stat["JVM"][tmp]={"RAM":[]}

             if float(k["MEM"])>float(config.get("contrainte", "mem")):
                stat["JVM"][tmp]["RAM"].append(k["MEM"])
                alert["RAM"]= "Allert !! RAM :  " + str(k["MEM"])+" JVM PID : " + str(k["Pid"])
             elif  (float(k["MEM"])!=0 or float(k["CPU"])!=0 ):
                stat["JVM"][tmp]["RAM"].append(k["MEM"])
             else :
                pass


def cpu_stats():
     for k in stats:
         tmp=k["Pid"]
         if  (float(k["MEM"])!=0.0 or float(k["CPU"])!=0.0 ):
             if  ((tmp  in  stat["JVM"].keys())):
                 if "CPU" in stat["JVM"][tmp]:
                     pass
                 else :
                     stat["JVM"][tmp]["CPU"]=[]

             else :
                stat["JVM"][tmp]={"CPU":[]}

             if ((float(k["CPU"]) > float(config.get("contrainte", "cpu")))) :
                stat["JVM"][tmp]["CPU"].append(k["CPU"])
                alert["CPU"]=  "Allert !! CPU :  " + str(k["CPU"]) +" JVM PID : " + str(k["Pid"])
             elif (float(k["MEM"])!=0 or float(k["CPU"])!=0 ):
                stat["JVM"][tmp]["CPU"].append(k["CPU"])
             else :
                pass

def  get_data():
    global alert
    global all_data
    global result
    info_jvm()
    cpu_stats()
    mem_stat()
    print stat
    """for k in all_data:
        for key,value in k.items():
            if value not in result.values():
                result[key] = value
    print result"""
    if len(alert.keys()) != 1 :
        send_alert(alert)
        alert={"type":"Alert"}

def send_alert(data):
    global alert
    u = "http://"+config.get("server","server_ip")+":"+config.get("server","server_port")+"/manager/VNFManager/passive"
    #r = requests.put("http://"+des["access_host"]["host ip"]+"/"+des["access_host"]["host port"]+"/api/vnf/update/", data=json.dumps(dict))
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(u, data=json.dumps(alert))
    #request.add_header('Content-Type', 'your/contenttype')
    request.get_method = lambda: 'GET'
    url = opener.open(request)


def send_data_all():
    global all_data
    global stat
    tmp={}
    tmp=stat
    stat={"JVM":{}}
    u = "http://"+config.get("server","server_ip")+":"+config.get("server","server_port")+"/manager/VNFManager/passive"
    #r = requests.put("http://"+des["access_host"]["host ip"]+"/"+des["access_host"]["host port"]+"/api/vnf/update/", data=json.dumps(dict))
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(u, data=json.dumps(tmp))
    #request.add_header('Content-Type', 'your/contenttype')
    request.get_method = lambda: 'GET'
    url = opener.open(request)
