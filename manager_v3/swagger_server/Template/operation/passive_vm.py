from  agent_vm import  *
import ConfigParser
import requests
import urllib2
import json
import pprint
import os
import socket
from collections import OrderedDict

config = ConfigParser.ConfigParser()
config.read(str(os.getcwd())+"/agent/api/builder/agent/config.conf")
#alert={"ip":socket.getfqdn(),"type":"VM"}
#data={"ip":socket.getfqdn(),"CPU":[],"type":"VM","RAM":[]}
data = OrderedDict()
alert = OrderedDict()


def init_data():
    data['CPU']=[]
    data['RAM']=[]
    data['id']=config.get('agent', 'id')

def init_alerts():
    alert['CPU']='GOOD'
    alert['RAM']='GOOD'
    alert['id']=config.get('agent', 'id')

def mem_stat():
     k=getRAM()
     if float(k["Usage_perc"])>float(config.get("contrainte", "mem")):
        data["RAM"].append(k["Usage_perc"])
        alert['RAM']= str("alert")
     else:
         data["RAM"].append(k["Usage_perc"])

def cpu_stat():
     TMP={}
     cores=getcpuload()
     for core in cores:
         if core["core"]=="cpu":
              TMP=core
              break
     if float(TMP["usage_perc"]) > float(config.get("contrainte", "cpu")):
         data["CPU"].append(TMP["usage_perc"])
         alert['CPU']=  str("alert")
     else:
          data["CPU"].append(TMP["usage_perc"])

def disk_stat():
     disks=getdiskUsage()
     stat_disk=[]
     disk_alerts=[]
     for disk in disks:
         if float(disk["usage_perc"]) >= float(config.get("contrainte", "disk")):
               disk_alerts.append("NOT GOOD")
               stat_disk.append({disk["file_system"]:disk["usage_perc"]})
               data["DISK"].append(stat_disk)
               alert["DISK"]=disk_alerts
         else :
               stat_disk.append({disk["file_system"]:disk["usage_perc"]})
               data["DISK"].append(stat_disk)

init_data()
init_alerts()

def  get_data():
    global alert
    global data
    cpu_stat()
    mem_stat()
    if ((alert["CPU"]!="GOOD") or (alert["RAM"]!="GOOD"))  :
        try:
            send_alert(alert)
        except:
            print "No data base configured or agent not up"
        send_alert_MM(alert)
        init_alerts()


def send_alert(data):
    u = "http://"+config.get("DB","alerts_url")+":"+config.get("DB","alerts_port")
    # some JSON:
    payload = [{'headers': {}, 'body': json.dumps(data,separators=(',',':')) }]
    headers = {'content-type': 'application/json'}
    response = requests.post(u, data=json.dumps(payload), headers=headers)

def send_alert_MM(data):
    u = 'http://'+config.get('server','server_ip')+':'+config.get('server','server_port')+'/swarmourr/manger/1.0.0/sensor/notification'
    # some JSON:
    payload = [{'headers': {}, 'body':data}]
    headers = {'content-type': 'application/json'}
    response = requests.post(u, data=json.dumps(payload), headers=headers)



def send_data_all():
    global data
    u = "http://"+config.get("DB","data_url")+":"+config.get("DB","data_port")
    payload = [{'headers': {}, 'body': json.dumps(data,separators=(',',':'))}]
    headers = {'content-type': 'application/json'}
    response = requests.post(u, data=json.dumps(payload), headers=headers)
    init_data()
