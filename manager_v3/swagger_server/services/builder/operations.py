import os
import subprocess
from time import sleep
import sys
import time
import datetime
import pprint
from decimal import Decimal
from collections import OrderedDict
import shutil
import errno
import inspect
from swagger_server.services.builder.agent_vm import *
from swagger_server.services.builder.agent_cnt import *
from swagger_server.services.builder.jvm_agents import *
import random
import string
import configparser
from swagger_server.services.builder.compresser import *
from swagger_server.services.deployer.connector import *
import requests
import urllib.request
#from snakebite.client import Client
import pprint
import ast
from datetime import datetime
from swagger_server.Template import agent_api_template
from swagger_server.services.builder.monitoringDB import * 
#---------------------------------------------------#
# __developper__  = "hamza safri"                   #
# __code_objectif__= "MONITORING MANAGER"           #
# __script_objectif__= "Create agent using json file#
# __language__    == "PYTHON  2.7"                  #
# --------------------------------------------------#

# define allowed char
chars = string.ascii_letters + string.digits
configs = configparser.ConfigParser()
configs.read(os.getcwd()+"/swagger_server/config.conf")
# create agent for vm env using admin descriptor parsed in  info dict
def create_vm_agent(info={}):
    config = configparser.ConfigParser()
    print(config)
    metric_code = ""
    metrics = []
    metric_exclude=[]
    mtr = info["_metrics"]
    host = info["_access_host"]
    print(mtr)
    print(host)
    for k, v in info["_metrics"].items():
        if v == True:
            metrics.append(k)
    print(metrics)
    id = ''.join(random.choice(chars) for x in range(8))
    name = "agent_vm_"+host["host ip"]+"_"+host["host port"]
    monitor_type=info["_agent"]["type"]

    # prepare template for agent
    copy(os.getcwd()+"/swagger_server/Template/agent_api_template", os.getcwd()+"/swagger_server/Template/agent_temp/"+name)
    copy(os.getcwd()+"/swagger_server/Template/operation/vm.py", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/")
    copy(os.getcwd()+"/swagger_server/Template/operation/agent_vm.py", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/impl/")
    copy(os.getcwd()+"/swagger_server/Template/operation/models/vm_model.py", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/models/")
    print( info["_agent"]["activated"])
    # create config file for agent
    config.add_section('host')
    config.set('host', 'ip', host["host ip"])
    config.set('host', 'port', host["host port"])
    config.set('host', 'type', host["type"])
    config.set('host', 'username', host["username"])
    config.set('host', 'password', host["password"])
    config.add_section('agent')
    config.set('agent', 'id', name)
    config.set('agent', 'metrics', ','.join(metrics))
    config.set('agent', 'type', info["_agent"]["type"])
    config.set('agent', 'activated', str(info["_agent"]["activated"]))
    config.add_section('server')
    config.set('server',"server_ip",host["server ip"])
    config.set('server',"server_port",host["server port"])
    config.add_section('DB')
    config.set('DB', 'alerts_url', info["_database"]["alerts"]["flume_url"])
    config.set('DB', 'alerts_port', info["_database"]["alerts"]["port"])
    config.set('DB', 'data_url', info["_database"]["data"]["flume_url"])
    config.set('DB', 'data_port', info["_database"]["data"]["port"])
    config.set('DB', 'hdfs_url', info["_database"]["hdfs"]["hdfs_url"])
    config.set('DB', 'hdfs_port', info["_database"]["hdfs"]["hdfs_port"])
    # add passive monitoring config
    if monitor_type.lower ()=="passive":
        config.add_section('contrainte')
        config.set('contrainte', 'mem', str(info["_agent_contrainte"]["mem"]))
        #config.set('contrainte', 'disk', info["agent contrainte"]["disk"])
        config.set('contrainte', 'cpu', str(info["_agent_contrainte"]["cpu"]))
        config.set('agent', 'refresh_period', str(info["_agent"]["refresh_period"]))
        copy(os.getcwd()+"/swagger_server/Template/operation/passive_vm.py", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/impl/")
        with open(os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/impl/"+"passive_vm.py") as f:
            line = f.readlines()
            for k,v in info["_agent_contrainte"].items():
                if float(v)==0:
                    metric_exclude.append(k)
            for i in range(len(metric_exclude)):
                find= "  "+metric_exclude[i]+"_stat()"
                for l in range(len(line)):
                    if find in line[l]:
                        line[l] = "#"+line[l]
            with open(os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/impl/"+"passive_vm.py", 'w') as f:
                for item in line:
                    f.write(item)
        update_pass("ENABLE",os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/app.py")


    with open(os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/config.conf", 'w') as set:
        config.write(set)

    # write different methods to collect ressources informations
    update("update", "ENABLE", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/vm.py")

    for metric in metrics:
        if metric == "net":
            metric_code += inspect.getsource(getNetTrBytes)
            metric_code += inspect.getsource(getlastVal)
            metric_code += inspect.getsource(getdebit)
            metric_code += inspect.getsource(getconnections)
            update("net", "ENABLE",os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/vm.py")
            update("connections", "ENABLE", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/vm.py")

        elif metric == "disk":
            metric_code += inspect.getsource(getdiskUsage)
            metric_code += inspect.getsource(getwrrd)
            update("disk", "ENABLE", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/vm.py")

        elif metric == "cpu":
            metric_code += inspect.getsource(getcpuload)
            metric_code += inspect.getsource(getcpuloadcore)
            update("cpu", "ENABLE", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/vm.py")

        elif metric == "mem":
            metric_code += inspect.getsource(getRAM)
            update("mem", "ENABLE", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/vm.py")
        else:
            return "No metric defined"

    # type of monitoring :
    copy(os.getcwd()+"/swagger_server/Template/agent_temp/"+name, "api/builder/"+name)

    # compresse agent
    compresse("api/builder/"+name)
    shutil.rmtree("api/builder/"+name)
    shutil.rmtree(os.getcwd()+"/swagger_server/Template/agent_temp/"+name)
    shutil.copy("api/builder/"+name+".tar.gz", os.getcwd()+"/swagger_server/Template/agent_temp/")
    os.remove("api/builder/"+name+".tar.gz")

    # send agent via ssh
    k=0
    k = deploy(os.getcwd()+"/swagger_server/Template/agent_temp/"+name+".tar.gz", host["host ip"], host["username"], info["_agent"]["activated"],host["password"])
    #add_conf(info)

# create agent for docker containe env


def create_cnt_agent(info={}):
    config = configparser.ConfigParser()
    metric_code = ""
    metric_exclude=[]
    metrics = []
    mtr = info["_metrics"]
    host = info["_access_host"]
    for k, v in info["_metrics"].items():
        if v == True:
            metrics.append(k)
    # id = ''.join(random.choice(chars) for x in range(8))
    name = "agent_cnt_"+host["host ip"]+"_"+host["host port"]
    monitor_type=info["_agent"]["type"]

    # prepare template for agent
    copy(os.getcwd()+"/swagger_server/Template/agent_api_template", os.getcwd()+"/swagger_server/Template/agent_temp/"+name)
    copy(os.getcwd()+"/swagger_server/Template/operation/cnt.py", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/")
    copy(os.getcwd()+"/swagger_server/Template/operation/agent_cnt.py", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/impl/")
    copy(os.getcwd()+"/swagger_server/Template/operation/models/vm_model.py", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/models/")

    # create config file for agent
    config.add_section('host')
    config.set('host', 'ip', host["host ip"])
    config.set('host', 'port', host["host port"])
    config.set('host', 'type', host["type"])
    config.set('host', 'username', host["username"])
    config.set('host', 'password', host["password"])
    config.add_section('agent')
    config.set('agent', 'id', name)
    config.set('agent', 'metrics', ','.join(metrics))
    config.set('agent', 'type', info["_agent"]["type"])
    config.set('agent', 'activated', str(info["_agent"]["activated"]))
    config.add_section('server')
    config.set('server',"server_ip",host["server ip"])
    config.set('server',"server_port",host["server port"])
    config.add_section('DB')
    config.set('DB', 'alerts_url', info["_database"]["alerts"]["flume_url"])
    config.set('DB', 'alerts_port', info["_database"]["alerts"]["port"])
    config.set('DB', 'data_url', info["_database"]["data"]["flume_url"])
    config.set('DB', 'data_port', info["_database"]["data"]["port"])
    config.set('DB', 'hdfs_url', info["_database"]["hdfs"]["hdfs_url"])
    config.set('DB', 'hdfs_port', info["_database"]["hdfs"]["hdfs_port"])

    # add passive monitoring config
    if monitor_type.lower ()=="passive":
        config.add_section('contrainte')
        config.set('contrainte', 'mem', str(info["_agent_contrainte"]["mem"]))
        #config.set('contrainte', 'disk', info["agent contrainte"]["disk"])
        config.set('contrainte', 'cpu', str(info["_agent_contrainte"]["cpu"]))
        config.set('agent', 'refresh_period', str(info["_agent"]["refresh_period"]))
        copy(os.getcwd()+"/swagger_server/Template/operation/passive_cnt.py", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/impl/")
        with open(os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/impl/passive_vm.py") as f:
            line = f.readlines()
            for k,v in info["_agent_contrainte"].items():
                if float(v)==0:
                    metric_exclude.append(k)
            for i in range(len(metric_exclude)):
                find= "  "+metric_exclude[i]+"_stat()"
                for l in range(len(line)):
                    if find in line[l]:
                        line[l] = "#"+line[l]
            with open(os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/impl/"+"passive_vm.py", 'w') as f:
                for item in line:
                    f.write(item)
        update_pass("ENABLE",os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/app.py")
    with open(os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/config.conf", 'w') as set:
        config.write(set)

    # write different methods to collect ressources informations
    metric_code += inspect.getsource(info_cnt)
    for metric in metrics:
        if metric == "net":
            metric_code += inspect.getsource(net_rx)
            metric_code += inspect.getsource(net_rx_byte)
            metric_code += inspect.getsource(net_rx_errors)
            metric_code += inspect.getsource(net_rx_dropped)
            metric_code += inspect.getsource(net_tx)
            metric_code += inspect.getsource(net_tx_byte)
            metric_code += inspect.getsource(net_tx_errors)
            metric_code += inspect.getsource(net_tx_dropped)
            metric_code += inspect.getsource(net_i_o)
            metric_code += inspect.getsource(getdebit)
            metric_code += inspect.getsource(getconnections)
            update("net", "ENABLE", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/cnt.py")
            update("connections", "ENABLE", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/cnt.py")
        elif metric == "disk":
            metric_code += inspect.getsource(disk_cnt)
            metric_code += inspect.getsource(getwrrd_cnt)
            update("disk", "ENABLE", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/cnt.py")

        elif metric == "cpu":
            metric_code += inspect.getsource(cpu)
            metric_code += inspect.getsource(cpu_c)
            metric_code += inspect.getsource(c_cpu)

            update("cpu", "ENABLE", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/cnt.py")

        elif metric == "mem":
            metric_code += inspect.getsource(mem_cnt)
            update("mem", "ENABLE", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/cnt.py")
        else:
            return "No metric defined"
    metric_code += inspect.getsource(agent_info)
    """try:
        f = open("agent_temp/"+name+"/api/impl/agent_cnt.py", 'a+')
        f.write(metric_code)
        f.close()
    except:
        return " can\'t create agent retry later """
    copy(os.getcwd()+"/swagger_server/Template/agent_temp/"+name, "api/builder/"+name)
    # compresse agent and send it via ssh
    compresse("api/builder/"+name)
    shutil.rmtree("api/builder/"+name)
    shutil.rmtree(os.getcwd()+"/swagger_server/Template/agent_temp/"+name)
    shutil.copy("api/builder/"+name+".tar.gz", os.getcwd()+"/swagger_server/Template/agent_temp/")
    os.remove("api/builder/"+name+".tar.gz")
    print(info["_agent"]["activated"])
    deploy("agent_temp/"+name+".tar.gz", host["host ip"], host["username"], info["_agent"]["activated"],host["password"])
    #add_conf(info)
    return "agent created"



# create agent to monitor jvm for vm and cnt docker


def create_jvm_agent(info={}):

    # copy("agent_api_template", "agent_temp/agent")
    config = configparser.ConfigParser()
    metric_code = ""
    metrics = []
    metric_exclude=[]
    mtr = info["_metrics"]
    host = info["_access_host"]
    for k, v in info["_metrics"].items():
        if v == True:
            metrics.append(k)
    name = "agent_jvm_"+host["host ip"]
    monitor_type=info["_agent"]["type"]

    # prepare template of jvm agent
    copy(os.getcwd()+"/swagger_server/Template/agent_api_template", os.getcwd()+"/swagger_server/Template/agent_temp/"+name)
    copy(os.getcwd()+"/swagger_server/Template/operation/jvm.py", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/")
    copy(os.getcwd()+"/swagger_server/Template/operation/jvm_agents.py", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/impl/")
    copy(os.getcwd()+"/swagger_server/Template/operation/models/vm_model.py", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/models/")

    # create config file for agent
    config.add_section('host')
    config.set('host', 'ip', host["host ip"])
    config.set('host', 'port', host["host port"])
    config.set('host', 'type', host["type"])
    config.set('host', 'username', host["username"])
    config.set('host', 'password', host["password"])
    config.add_section('agent')
    config.set('agent', 'id', name)
    config.set('agent', 'metrics', ','.join(metrics))
    config.set('agent', 'type', info["_agent"]["type"])
    config.set('agent', 'activated', info["_agent"]["activated"])
    config.add_section('server')
    config.set('server',"server_ip",host["server ip"])
    config.set('server',"server_port",host["server port"])
    # add passive monitoring config
    if monitor_type.lower ()=="passive":
        config.add_section('contrainte')
        config.set('contrainte', 'mem', info["_agent_contrainte"]["mem"])
        #config.set('contrainte', 'disk', info["agent contrainte"]["disk"])
        config.set('contrainte', 'cpu', info["_agent_contrainte"]["cpu"])
        config.set('agent', 'refresh_period', info["agent"]["refresh_period"])
        copy(os.getcwd()+"/swagger_server/Template/operation/passive_jvm.py", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/impl/")
        with open(os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/impl/"+"passive_jvm.py") as f:
            line = f.readlines()
            for k,v in info["_agent_contrainte"].items():
                if float(v)==0:
                    metric_exclude.append(k)
            for i in range(len(metric_exclude)):
                find= "  "+metric_exclude[i]+"_stat()"
                for l in range(len(line)):
                    if find in line[l]:
                        line[l] = "#"+line[l]
            with open(os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/impl/"+"passive_jvm.py", 'w') as f:
                for item in line:
                    f.write(item)
        update_pass("ENABLE",os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/app.py")

    with open(os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/config.conf", 'w') as set:
        config.write(set)

    #  create methods to collect ressorces informations
    for metric in metrics:
        if metric.lower() == "connections":
            metric_code += inspect.getsource(get_connections)
            update("connections", "ENABLE", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/jvm.py")
        elif metric.lower() == "gc":
            metric_code += inspect.getsource(get_gc)
            update("gc", "ENABLE", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/jvm.py")
        elif metric.lower() == "threads":
            metric_code += inspect.getsource(get_threads)
            metric_code += inspect.getsource(cmd1)
            update("threads", "ENABLE", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/jvm.py")
        elif metric.lower() == "ressouces":
            metric_code += inspect.getsource(info_m)
            update("ressources", "ENABLE", os.getcwd()+"/swagger_server/Template/agent_temp/"+name+"/api/endpoint/jvm.py")
    """    try:
        f = open("agent_temp/"+name+"/api/impl/jvm_agents.py", 'a+')
        f.write(metric_code)
        f.close()
    except:
    return " can\'t create agent retry later """
    # compress and send it  via SSH
    copy(os.getcwd()+"/swagger_server/Template/agent_temp/"+name, "api/builder/"+name)
    compresse("api/builder/"+name)
    shutil.rmtree("api/builder/"+name)
    shutil.rmtree(os.getcwd()+"/swagger_server/Template/agent_temp/"+name)
    shutil.copy("api/builder/"+name+".tar.gz", os.getcwd()+"/swagger_server/Template/agent_temp/")
    os.remove("api/builder/"+name+".tar.gz")
    deploy(os.getcwd()+"/swagger_server/Template/agent_temp/"+name+".tar.gz", host["host ip"], host["username"], info["_agent"]["activated"],host["password"])
    return "agent created"

# method agent osgi builder
def create_osgi_agent(info={}) :
        deploy_http(info)
        #add_conf(info)

# method start  agent osgi
def enable_agents_osgi(info={}) :
        deploy_http_start(info)

# method  stop agent osgi
def disable_agents_osgi(info={}) :
        deploy_http_stop(info)

# method update agent osgi
def update_agents_osgi(info={}) :
        deploy_http_update(info)
        
# method delete agent osgi
def delete_agents_osgi(info={}) :
        deploy_http_delete(info)
        #delete_agent_db_osgi(info)

# method ro copy file and directory
def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # si une erreur existe
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)

def delete_agent_db_osgi(info={}):
    tmp=configs.get("DB","hdfs").split(":")
    client = Client(tmp[0],int(tmp[1]))
    for p in client.delete(['/monitoring/datas/type=jvm/provider='+info["host ip"]],recurse=True):
	       print("")

# methode to update agent metrics
def update(name, op, file):
    line = []
    find = "@ns.route('/" + name
    with open(file) as f:
        line = f.readlines()
    if op == "ENABLE":
        find = "# "+find
        for l in range(len(line)):
            if find in line[l]:
                line[l] = line[l][2:]

    elif op == "DISABLE":
        for l in range(len(line)):
            if find in line[l]:
                line[l] = "# "+line[l]

    with open(file, 'w') as f:
        for item in line:
            f.write(item)
        return 204
    return 202




def update_pass(op,file):
    line = []
    with open(file) as f:
        line = f.readlines()
    if op == "ENABLE":
        find = "#app.apscheduler.add_job"
        for l in range(len(line)):
            if find in line[l]:
                line[l] = line[l][1:]

    elif op == "DISABLE":
        find = "app.apscheduler.add_job"
        for l in range(len(line)):
            if find in line[l]:
                line[l] = "#"+line[l]

    with open(file, 'w') as f:
        for item in line:
            f.write(item)
        return 204
    return 202


def update_agent(des):
    dict = {"enable": [], "disable": [],"contraint":{},"host":{}}
    for k, v in des["_metrics"].items():
        if v == True:
            dict["enable"].append(k)
        else:
            dict["disable"].append(k)
    dict["contraint"]=des["_agent_contrainte"]
    dict["host"]=des["_access_host"]
    u = "http://"+des["_access_host"]["host ip"]+":"+des["_access_host"]["host port"]+"/api/vnf/update"
    req=urllib.request.Request(url=u, data=json.dumps(dict).encode('utf-8'),method='PUT')
    rsp= urllib.request.urlopen(req)

def update_agent_cnt(des):
    dict = {"enable": [], "disable": [],"contraint":{},"host":{}}
    for k, v in des["_metrics"].items():
        if v == True:
            dict["enable"].append(k)
        else:
            dict["disable"].append(k)
    dict["contraint"]=des["_agent_contrainte"]
    dict["host"]=des["_access_host"]
    u = "http://"+des["_access_host"]["host ip"]+":"+des["_access_host"]["host port"]+"/api/vnf/update/"
    r = requests.put(u, data=json.dumps(dict))


def update_agent_anf(des):
    dict = {"enable": [], "disable": []}
    for k, v in des["_metrics"].items():
        if v == True:
            dict["enable"].append(k)
        else:
            dict["disable"].append(k)



    u = "http://"+des["_access_host"]["host ip"]+":"+des["_access_host"]["host port"]+"/api/jvm/update/"
    #r = requests.put("http://"+des["access_host"]["host ip"]+"/"+des["access_host"]["host port"]+"/api/vnf/update/", data=json.dumps(dict))

    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(u, data=json.dumps(dict))
    #request.add_header('Content-Type', 'your/contenttype')
    request.get_method = lambda: 'PUT'
    url = opener.open(request)


def delete_agents(info={}):
    #delete_agent_db(info)
    delete_agent(info["_host_ip"],info["_username"],info["_password"])


def delete_agent_db(info={}):
    tmp=configs.get("DB","hdfs").split(":")
    client = Client(tmp[0],int(tmp[1]))
    for p in client.delete(['/monitoring/datas/type='+info["type"]+'/provider='+info["host ip"]],recurse=True):
	       print("")

def disable_agents(info={}):
    disable_agent(info["_host_ip"],info["_username"],info["_password"])

def enable_agents(info={}):
    enable_agent(info["_host_ip"],info["_username"],info["_password"])

def update_pass(op,file):
    line = []
    with open(file) as f:
        line = f.readlines()
    if op == "ENABLE":
        find = "#app.apscheduler.add_job"
        for l in range(len(line)):
            if find in line[l]:
                line[l] = line[l][1:]

    elif op == "DISABLE":
        FIND = "app.apscheduler.add_job"
        for l in range(len(line)):
            if find in line[l]:
                line[l] = "#"+line[l]

    with open(file, 'w') as f:
        for item in line:
            f.write(item)
        return 204
    return 202



def store_data(data):
    url_flume = 'http://'+configs.get("DB","data")
    # some JSON:
    payload = [{'headers': {}, 'body': json.dumps(data,separators=(',', ':')) }]
    headers = {'content-type': 'application/json'}
    response = requests.post(url_flume, data=json.dumps(payload), headers=headers)


def store_alerts(data):
    url_flume = 'http://'+configs.get("DB","alerts")
    # some JSON:
    payload = [{'headers': {}, 'body': json.dumps(data,separators=(',', ':')) }]
    headers = {'content-type': 'application/json'}
    response = requests.post(url_flume, data=json.dumps(payload), headers=headers)



def get_stored_data(data_path):
    tmp=configs.get("DB","hdfs").split(":")
    client = Client(tmp[0],int(tmp[1]))
    path=[]
    dict=[]
    for x in client.ls([data_path]):
        if (".tmp" in x["path"])==False:
            path.append(x["path"])

    for l in client.text(path):
          try:
              dict.append(ast.literal_eval(l))
          except:
              pass
    return dict

def get_stored_numbre(data_path):
    tmp=configs.get("DB","hdfs").split(":")
    client = Client(tmp[0],int(tmp[1]))
    return len(list(client.ls([data_path])))


def get_stored_provider(data_path):
    tmp=configs.get("DB","hdfs").split(":")
    client = Client(tmp[0],int(tmp[1]))
    path=[]
    for x in client.ls([data_path]):
        if (".tmp" in x["path"])==False:
            path.append((x["path"].split("="))[2])
    return path

def config_server(info={}):
    configs.set('DB', 'alerts', info["alerts"]["flume_url"]+":"+info["alerts"]["port"])
    configs.set('DB', 'data', info["data"]["flume_url"]+":"+info["data"]["port"])
    configs.set('DB', 'hdfs', info["hdfs"]["hdfs_url"]+":"+info["hdfs"]["hdfs_port"])
    with open(os.getcwd()+"/config.conf", 'w') as set:
            configs.write(set)

def get_stored_data(data_path):
    tmp=configs.get("DB","hdfs").split(":")
    client = Client(tmp[0],int(tmp[1]))
    path=[]
    dict1=[]
    times=[]
    ram=[]
    cpu=[]
    date_send=[]
    while not("hours" in data_path):
        for x in client.ls([data_path]):
            path.append((x["path"]))
            data_path=path[-1]
    path=[]
    for x in client.ls([data_path]):
        if (".tmp" in x["path"])==False:
            path.append(x["path"])
        tmp=str(x["path"]).split("/")
        date_str = tmp[-1]
        date= (date_str.split("data")[1][0:17]).replace("." ,"-")
        times.append(datetime.strptime(date, '%y-%m-%d-%H-%M-%S'))

    for l in client.text(path):
              dict1.append(l)
    for t in range(len(times)) :
        date_send.append(myconverter(times[t]))

    k=dict1[-40::2]
    v=date[-40::2]
    for i in range(len(k)):
        for j in range(len(k[i].split("\n"))-1):
            tmp = [float(m) for m in (ast.literal_eval((k[i].split("\n"))[j])["CPU"])]
            ram.append(sum(ast.literal_eval((k[i].split("\n"))[j])["RAM"])/len(ast.literal_eval((k[i].split("\n"))[j])["RAM"]))
            cpu.append(sum(tmp)/len(tmp))


    return  {"ram":ram,"cpu":cpu,"time":date_send[-40::2]}

def get_stored_data_hour(data_path):
    tmp=configs.get("DB","hdfs").split(":")
    client = Client(tmp[0],int(tmp[1]))
    tmp = []
    times = []
    ram = []
    cpu = []
    path = []
    data = []
    data_c = []
    data_r = []
    time_f = []
    state = True
    while not 'days' in data_path:
        for x in client.ls([data_path]):
            path.append(x['path'])
            data_path = path[-1]

    path = []
    dict1 = []

    for x in client.ls([data_path]):
        if 'hours' in x['path']:
            path.append(x['path'])

    for pth in path:
        for x in client.ls([pth]):
            if ('.tmp' in x['path']) == False:
                data.append(x['path'])
                tmp = str(x['path']).split('/')
                date_str = tmp[-1]
                date = (date_str.split('data')[1])[0:17].replace('.', '-')
                times.append(datetime.strptime(date, '%y-%m-%d-%H-%M-%S'))
        tmp = []
        tmp.append(data[-1])
        for l in client.text(tmp):
            dict1.append(l)
        k = dict1[-1:]
        for i in range(len(k)):
            for j in range(len(k[i].split('\n')) - 1):
                tmp = [float(m) for m in ast.literal_eval(k[i].split('\n')[j])['CPU']]
                ram.append(sum(ast.literal_eval(k[i].split('\n')[j])['RAM'])/len(ast.literal_eval(k[i].split('\n')[j])['RAM']))
                cpu.append(sum(tmp)/len(tmp))
        data_c.append(cpu[-1])
        data_r.append(ram[-1])
        time_f.append(myconverter(times[-1]))
        data=[]
        cpu=[]
        ram=[]
    return {'ram': data_r, 'cpu': data_c, 'time': time_f}


def myconverter(o):
    if isinstance(o,datetime):
        tmp=datetime.strftime(o,"%y-%m-%d-%H-%M-%S")
        return time.mktime(datetime.strptime(tmp, '%y-%m-%d-%H-%M-%S').timetuple())*1000

def add_conf(data):
    tmp=configs.get("DB","conf").split(":")
    u = "http://"+tmp[0]+":"+tmp[1]
    # some JSON:
    payload = [{'headers': {}, 'body': json.dumps(data,separators=(',',':')) }]
    headers = {'content-type': 'application/json'}
    response = requests.post(u, data=json.dumps(payload), headers=headers)
