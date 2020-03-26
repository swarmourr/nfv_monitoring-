#! /usr/bin/python
from paramiko import SSHClient
import paramiko
from scp import SCPClient
import requests
from swagger_server.services.deployer.configure import *
import configparser
import os
import json
import time
'''
 Read configuration from file configuration
'''
config = configparser.ConfigParser()

'''
ssh  connection
    ip : host address ip
    username : username to use 
    
'''
def connect_ssh(ip, username, *path):
    config.read(os.getcwd()+"/config.conf")
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    ssh.connect(ip, port=int(config.get("ssh","port")), username=username, password="", key_filename=config.get("ssh","key"),timeout=30)
    return ssh

'''
deploy agent in VM or container 
    ip : host address ip
    username : username to use
    State: enable or disable the agent during the installation
    
'''
def deploy(name, ip, username, state):
    if username == "root":
        path = "root"
    else:
        path = "home/"+username
    ssh = connect_ssh(ip, username, path)
    # SCPCLient takes a paramiko transport as an argument
    ssh.exec_command("mkdir /"+path+"/agent/")
    scp = SCPClient(ssh.get_transport())
    # Uploading the 'test' directory with its content in the
    scp.put(name, recursive=True, remote_path='/'+path+'/agent')
    r = name.split("/")[1]
    if state == True:
        installer(ssh, path, r)
        scp.close()
        ssh.close()
    elif state == False:
        ssh.close()
        scp.close()
    return "pid"

'''
deploy agent in OSGI envirement 
    info : containe all informations about the envirement 
        host ip : address ip of apache felix
        host port  : port used by apache felix 
    
'''
def deploy_http(info={}):

    filename = 'operation/fr.laas.anf.agent_1.0.0.201908052142.jar'
    url_agent= 'http://'+ info["access_host"]["host ip"]+':'+info["access_host"]["host port"]+'/system/console/bundles'
    url_config= 'http://'+  info["access_host"]["host ip"]+':'+ info["access_host"]["host port"]+'/services/config'
    files = {'bundlefile':(filename, open(filename, 'rb'), "multipart/form-data")}
    data = {
        'action': 'install',
        'bundlestart': "true"
        }
    requests.post(url_agent, files=files, data=data, auth=( info["access_host"]["username"], info["access_host"]["password"]))
    time.sleep(3)
    requests.post(url_config, data=json.dumps(info))


'''
start-stop-update delete deployed agent in OSGI envirement 
    info : containe all informations about the envirement 
        host ip : address ip of apache felix
        host port  : port used by apache felix 
    
'''
def deploy_http_start(info={}):
    url_agent= 'http://'+ info["host ip"]+':'+info["host port"]+'/system/console/bundles/fr.laas.anf.agent'
    data = {
        'action': 'start',
        }
    requests.post(url_agent, data=data, auth=( info["username"], info["password"]))


def deploy_http_stop(info={}):
    url_agent= 'http://'+ info["host ip"]+':'+info["host port"]+'/system/console/bundles/fr.laas.anf.agent'
    data = {
        'action': 'stop',
        }
    requests.post(url_agent, data=data, auth=( info["username"], info["password"]))

def deploy_http_update(info={}):
    url_config= 'http://'+  info["access_host"]["host ip"]+':'+ info["access_host"]["host port"]+'/services/config'
    r=requests.post(url_config, data=json.dumps(info))

def deploy_http_delete(info={}):
    url_agent= 'http://'+ info["host ip"]+':'+info["host port"]+'/system/console/bundles/fr.laas.anf.agent'
    data = {
        'action': 'uninstall',
        }
    requests.post(url_agent, data=data, auth=( info["username"], info["password"]))

'''
enable-disable-update delete deployed agent in virtual envirement (VM-CNT) 
      
'''

def delete_agent(ip,username):
        if username == "root":
            path = "root"
        else:
            path = "home/"+username
        ssh=connect_ssh(ip,username,path)
        delete(ssh,path)



def disable_agent(ip,username):
    if username == "root":
        path = "root"
    else:
        path = "home/"+username
    ssh=connect_ssh(ip,username,path)
    disable(ssh,path)


def enable_agent(ip,username):
    if username == "root":
        path = "root"
    else:
        path = "home/"+username

    ssh=connect_ssh(ip,username,path)
    enable(ssh,path,ip)

'''
Function to deploy custom vnf agent (support python flask rest plus api)

    ip : host ip 
    username : host ssh username used 
    path : absolute path to agent  

     
'''

def deploy_custom( ip, username, path):
    ssh = connect_ssh(ip, username, path)
    scp = SCPClient(ssh.get_transport())
    scp.put(path, recursive=True, remote_path="/home/"+username+"/")
    way = str(absoluteFilePaths(path)).split("/")[-2:]
    enable_costum(ssh,"/home/"+username+"/"+way[-2]+"/"+way[-1])
    scp.close()
    ssh.close()
    return "pid"

def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           if f == "app.py":
               return  os.path.abspath(os.path.join(dirpath,f))
