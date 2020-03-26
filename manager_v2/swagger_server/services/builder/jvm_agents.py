#--------------------------------------------------------#
# __developper__  = "hamza safri"                        #
# __code_objectif__= "monitoring jvm consumption"        #
# __language__    == "PYTHON  3"                         #
# __github__ == "Swarmourr"                              #
#--------------------------------------------------------#

import os
import subprocess
import re
import pprint
from collections import OrderedDict
import json
from subprocess import call

'''
get general information about the jvm
    uptime 
    ID
    memory
    HOSTNAME 

'''
def info_m():
    p = subprocess.Popen('jps -vl | grep -vi Jps |awk \'{#print$1}\'   ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    l = p.stdout.readlines()
    jvm = []
    for i in range(len(l)):
        pid = l[i].rstrip('\n')
        k = subprocess.Popen('ps -eo pid,ppid,%mem,%cpu,rss,vsz,etime,cmd |grep '+pid + '|grep -vi grep ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        n = subprocess.Popen('jstat -gc ' + pid + ' | awk \'{split($0,a,\" \"); #printa[3]+a[4]+a[6]+a[8]}\' ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        info = re.sub(' +', ' ', k.stdout.readlines()[0].rstrip('\n'))
        tmp = (info.strip()).split(" ")
        jvm.append(OrderedDict({'Pid':  int(tmp[0]), 'PPid': int(tmp[1]), 'Uptime': tmp[6], 'MEM': float(tmp[2]), "Heap_mem_K": float(n.stdout.readlines()[1].rstrip('\n')), "CPU": float(tmp[3]), "RSS_K": float(tmp[4]), "VSZ_K": float(tmp[5]), 'CMD': " ".join(tmp[7:])}))
    return jvm

'''
get connections established by  the jvm

'''

def get_connections():
    p = subprocess.Popen('jps -vl | grep -vi Jps |awk \'{#print$1}\'   ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    l = p.stdout.readlines()
    jvm = []
    cnx = OrderedDict({'TCP': {}, 'UDP': {}, "Total": 0})
    final = {}
    for i in range(len(l)):
        cnx["Total"] = 0
        p1 = subprocess.Popen('lsof -i -a -p ' + str(l[i]).rstrip() + '| awk \'{#print $8,$9}\'|grep -v NAME', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = p1.stdout.readlines()
        tmp_key = []
        for j in range(len(lines)):
            k = lines[j].split(":")
            #printk
            if k[0][:3] in cnx.keys():
                cnx["Total"] = cnx["Total"] + 1
                if k[-1].rstrip() in tmp_key:
                    #cnx[k[0][:3]][k[-1].rstrip()]["nbr"] = cnx[k[0][:3]][k[-1].rstrip()]["nbr"]+1
                    cnx[k[0][:3]][k[-1].rstrip()]["connection"].append((lines[j].split(" "))[1].rstrip())
                else:
                    tmp_key.append(k[-1].rstrip())
                    cnx[k[0][:3]][k[-1].rstrip()] = OrderedDict({"connection": (lines[j].split(" "))[1].rstrip()})

            else:
                tmp_key.append(k[-1].rstrip())
                #cnx[k[0][:3]][k[-1].rstrip()] = OrderedDict({"nbr": 1, "connection": [(lines[i].split(" "))[1].rstrip()]})
                cnx[k[0][:3]][k[-1].rstrip()] = OrderedDict({"connection": [(lines[j].split(" "))[1].rstrip()]})

        final.update({str(l[i]).rstrip(): cnx})
    return {"opened connections": final}

'''
get all thread of jvm

'''

def get_threads():
    p = subprocess.Popen('jps -vl | grep -vi Jps |awk \'{#print$1}\'   ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    l = p.stdout.readlines()
    for i in range(len(l)):
        p1 = subprocess.Popen('jstack ' + str(l[i]).rstrip() + ' |grep nid=* | tr -s  \" \"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        l1 = p1.stdout.readlines()
        threads = []
        for string in l1:
            #printl1
            name = re.search('"(.*)"', string)
            name = name.group(0).replace('"', "")
            nid_hex = re.search('nid=(.*) ', string)
            number = str(int((nid_hex.group(1).split())[0], 16))
            tmp = cmd1(str(l[i]).rstrip(), number)[0].split()
            threads.append(OrderedDict({"Pid":   str(l[i]).rstrip(), "Tid": number, "Thread name":  name, "Thread MEM": float(tmp[0]), "Thread CPU": float(tmp[1])}))
        return threads


def cmd1(pids, nid):
    sk = []
    if pids != "":
        p = subprocess.Popen('ps H -o pid,tid,cmd,comm,%mem,%cpu -p ' + pids + ' |grep  ' + str(nid) + ' |awk \'{#print$(NF-1) \"  \"  $NF}\'', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        sk = p.stdout.readlines()
    if len(sk) != 0:
        return sk
    return sk

'''
get general information about the  gc of jvm
     

'''
def get_gc():
    p = subprocess.Popen('jps -vl | grep -vi Jps |awk \'{#print$1}\'   ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    l = p.stdout.readlines()
    gc = []
    for i in range(len(l)):
        pid = l[i].rstrip('\n')
        n = subprocess.Popen('jstat -gc ' + pid + '| grep -iv s0 ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        tmp = (n.stdout.readlines())[0].split()
        #printtmp[18]
        gc.append({pid: {"Surviver 0": {"Capacity": tmp[0], "Utilization": tmp[2], "Pctg": round((float(tmp[2].replace(",", "."))/float(tmp[0].replace(",", ".")))*100 if float(tmp[0].replace(",", ".")) else 0, 3)},
                         "Surviver 1": {"Capacity": tmp[1], "Utilization": tmp[3], "Pctg": round((float(tmp[3].replace(",", "."))/float(tmp[1].replace(",", ".")))*100 if float(tmp[1].replace(",", ".")) else 0, 3)},
                         "Eden space": {"Capacity": tmp[4], "Utilization": tmp[5], "Pctg": round((float(tmp[5].replace(",", "."))/float(tmp[4].replace(",", ".")))*100 if float(tmp[4].replace(",", ".")) else 0, 3)},
                         "Old space": {"Capacity": tmp[6], "Utilization": tmp[7], "Pctg": round((float(tmp[7].replace(",", "."))/float(tmp[6].replace(",", ".")))*100 if float(tmp[7].replace(",", ".")) else 0, 3)},
                         "Metaspace": {"Capacity": tmp[8], "Utilization": tmp[9], "Pctg": round((float(tmp[9].replace(",", "."))/float(tmp[8].replace(",", ".")))*100 if float(tmp[8].replace(",", ".")) else 0, 3)},
                         "Compressed Class space": {"Capacity": tmp[10], "Utilization": tmp[11], "Pctg": round((float(tmp[11].replace(",", "."))/float(tmp[10].replace(",", ".")))*100 if float(tmp[10].replace(",", ".")) else 0, 3)},
                         "Young Generation Collections ": {"Number ": tmp[12], "Accumlated Time": tmp[13], " YG Time": round((float(tmp[13].replace(",", "."))/float(tmp[12].replace(",", ".")))*100 if float(tmp[12].replace(",", ".")) else 0, 5)},
                         "Full GC": {"Number ": tmp[14], "Accumlated Time": tmp[15], " GC Time": round((float(tmp[15].replace(",", "."))/float(tmp[14].replace(",", ".")))*100 if float(tmp[14].replace(",", ".")) else 0, 5)},
                         "Concurent GC": {"Number ": tmp[16], "Accumlated Time": tmp[17]},
                         "GC Time": tmp[18]
                         }})

    return gc
