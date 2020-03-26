import os
import paramiko
import socket


'''
installation  agent in VM or container 
    name: name of the agent zip
    path : installation directory location
     
'''
def installer(ssh, path, name):
    print(path)
    print(name)
    cmd = "tar xzvf /"+path+"/agent/"+name + " -C /"+path+"/agent/"
    print(cmd)
    mv = "mv /"+path+"/agent/api/builder/* /"+path+"/agent/api/builder/agent/"
    pip = "pip install -r /"+path+"/agent/api/builder/agent/req.txt"
    start = "python /"+path+"/agent/api/builder/agent/app.py&"
    pid = "ps -A -O pid  |grep \"/usr/bin/python /"+path+"/agent/api/builder/agent/app.py\" |grep -v grep | tr -s \"  \" |cut -d\" \" -f 1"
    stdin, stdout,stderr=ssh.exec_command("script /dev/null")
    stdin, stdout,stderr=ssh.exec_command("screen")
    print(stdout.readlines())
    stdin, stdout,stderr=ssh.exec_command(cmd)
    print(stdout.readlines())

    stdin, stdout,stderr=ssh.exec_command(mv)
    print(stdout.readlines())
    stdin, stdout,stderr=ssh.exec_command(pip)
    print(stdout.readlines())
    print(start)
    stdin, stdout,stderr=ssh.exec_command(start,timeout=10)
    print(stdout.readlines())
    """try:
     print("")   
    except socket.timeout:
        pass
    stdin, stdout,stderr=ssh.exec_command(pid)"""
    
'''
delete agent deployed  in VM or container 
    name: name of the agent zip
    path : installation directory location
     
'''
def delete(ssh,path):
    cmd = "for pid in $(ps -ef | grep \"/" + path + "/agent/api/builder/agent/app.py\" | awk '{print $2}'); do kill -9 $pid; done"
    rmv= "rm -rf /"+path+"/agent"
    stdin, stdout,stderr=ssh.exec_command(cmd)
    print(stdout.readlines())
    stdin, stdout,stderr=ssh.exec_command(rmv)
    print(stdout.readlines())


'''
disable  agent deployed  in VM or container 
    name: name of the agent zip
    path : installation directory location
     
'''
def disable(ssh,path):
    cmd = "for pid in $(ps -ef | grep \"/" + path + "/agent/api/builder/agent/app.py\" | awk '{print $2}'); do kill -9 $pid; done"
    stdin, stdout,stderr=ssh.exec_command(cmd)
    print(stdout.readlines())
    
'''
enable  agent deployed  in VM or container 
    name: name of the agent zip
    path : installation directory location
     
'''
def enable(ssh,path,ip):
    tst=[]
    test="[ -d \"/"+path+"/agent/api\" ] && echo \"TRUE\""
    start = "python /"+path+"/agent/api/builder/agent/app.py"
    stdin, stdout,stderr=ssh.exec_command(test)
    tst=stdout.readlines()
    if len(tst)!=0:
        if tst[0].rstrip()=="TRUE":
            try:
                stdin, stdout,stderr=ssh.exec_command(start,timeout=3)
                print(stdout.readlines())
            except socket.timeout:
                pass
        else :
             print("something wrong")
    else:
        installer(ssh,path,"agent_vm_"+ip +".tar.gz")

def enable_costum(ssh,agent):
        start = "python " + agent
        try:
            stdin, stdout,stderr=ssh.exec_command(start,timeout=3)
            print(stdout.readlines())
        except socket.timeout:
            pass
