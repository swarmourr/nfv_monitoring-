import os
import subprocess
from time import sleep
import sys
import time
import datetime
import pprint
from decimal import Decimal
from collections import OrderedDict
import ConfigParser
import platform
#------------------------------------------------#
# __developper__  = "hamza safri"                #
# __code_objectif__= "monitoring VM consumption" #
# __language__    == "PYTHON  2.7"               #
# -----------------------------------------------#
prv_mon_data = {}

config = ConfigParser.ConfigParser()
config.read(str(os.getcwd())+"/agent/api/builder/agent/config.conf")

def get_info():
    dict={'system':{'Platform': platform.platform(),
                    'system': platform.system(),
                    'node': platform.node(),
                    'release': platform.release(),
                    'version': platform.version(),
                    'machine': platform.machine(),
                    'processor': platform.processor(),
                    'Arch': platform.architecture()[0]}
                    }
    return dict

def getRAM():
    '''
    get freeRAM anf Total memory from /proc/meminfo du OS de VM
    '''
    meminfo = dict((i.split()[0].rstrip(':'), int(i.split()[1])) for i in open('/proc/meminfo').readlines())
    return {"TotalRAM KB ": meminfo["MemTotal"], "FreeRam KB ": meminfo["MemFree"], "Usage_perc": (100-round(((float(meminfo["MemFree"])+float(meminfo["Cached"])+float(meminfo["Buffers"]))/float(meminfo["MemTotal"]))*100, 3))}


def getcputime():
    '''
    get cpu consumption from /proc/stat du OS de VM
    '''
    cpustat = '/proc/stat'
    sep = ' '
    cpu_infos = {}
    with open(cpustat, 'r') as f_stat:
        lines = [line.split(sep) for content in f_stat.readlines() for line in content.split('\n') if line.startswith('cpu')]

        for cpu_line in lines:
            if '' in cpu_line:
                cpu_line.remove('')  # remove empty elements
            cpu_line = [cpu_line[0]]+[float(i) for i in cpu_line[1:]]  # type casting
            cpu_id, user, nice, system, idle, iowait, irq, softrig, steal, guest, guest_nice = cpu_line
            Idle = idle+iowait
            NonIdle = user+nice+system+irq+softrig+steal

            Total = Idle+NonIdle

            cpu_infos.update({cpu_id: {'total': Total, 'idle': Idle}})
        return cpu_infos


def getcpuload():
    '''
    CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)
    '''
    start = getcputime()
    sleep(1)
    stop = getcputime()

    usage = []
    for cpu in start:
        Total = stop[cpu]['total']
        PrevTotal = start[cpu]['total']

        Idle = stop[cpu]['idle']
        PrevIdle = start[cpu]['idle']
        CPU_Percentage = ((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)*100
        usage.append({"core": cpu, "usage_perc": str(round(CPU_Percentage, 2))})
    return usage


def getcpuloadcore(name):
    '''
    CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)
    '''
    start = getcputime()
    sleep(1)
    stop = getcputime()

    usage = []
    for cpu in start:
        Total = stop[cpu]['total']
        PrevTotal = start[cpu]['total']

        Idle = stop[cpu]['idle']
        PrevIdle = start[cpu]['idle']
        CPU_Percentage = ((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)*100
        usage.append({"core": cpu, "usage_perc": str(round(CPU_Percentage, 2))})
    for n in usage:
        if name in n["core"]:
            return n


def getdiskUsage(*name):
    '''
    get  all disk and  consumption in vm using df command
    '''
    if (len(name) != 0 and name[0] != ""):
        p = subprocess.Popen('df -h /dev/' + str(name[0]), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        p = subprocess.Popen('df -h', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = p.stdout.readlines()
    disks = []
    disk_info = []
    count = 0
    for line in lines:
        count += 1
        if count < 2:
            continue
        dk = line.split()
        if dk[0] == 'none':
            continue
        print dk
        disk = OrderedDict()
        disk_info = getwrrd(dk[0])
        disk["file_system"] = dk[0]
        disk["size_total"] = dk[1]
        disk["used"] = dk[2]
        disk["free"] = dk[3]
        disk["usage_perc"] = (dk[4].decode("utf-8")).replace('%', '')
        disk["tps"] = disk_info[1]
        disk["read KB/s"] = disk_info[2]
        disk["write KB/s"] = disk_info[3]
        disk["read KB"] = disk_info[4]
        disk["write KB"] = disk_info[5]
        disks.append(disk)
    return disks


def getNetTrBytes(*name):
    '''
    get  all networks interfaces in vm using df command
    '''
    # prv_mon_data = {}

    if (len(name) != 0 and name[0] != ""):
        p = subprocess.Popen('cat /proc/net/dev |grep ' + str(name[0]), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = p.stdout.readlines()
        netifs = []
        count = 0
        for line in lines:
            nif = line.split()
            netif = OrderedDict()
            nif[0] = (nif[0].decode("utf-8")).replace(':', '')
            netif["interface"] = nif[0]
            netif["rx_b"] = int(nif[1])
            netif["tx_b"] = int(nif[9])
            netif["rx_pks"] = int(nif[2])
            netif["tx_pks"] = int(nif[10])
            netif["rx_error"] = int(nif[3])
            netif["rx_drops"] = int(nif[4])
            netif["tx_error"] = int(nif[11])
            netif["tx_drops"] = int(nif[12])
        # RX pkts per sec
            lv = int(getlastVal(nif[0], "rx_pks"))
            if lv != -1:
                netif["rx_pps"] = int(nif[2]) - lv
            else:
                netif["rx_pps"] = -1
        # TX pkts per sec
            lv = int(getlastVal(nif[0], "tx_pks"))
            if lv != -1:
                netif["tx_pps"] = int(nif[10]) - lv
            else:
                netif["tx_pps"] = -1
        # RX Bytes per sec
            lv = int(getlastVal(nif[0], "rx_b"))
            if lv != -1:
                netif["rx_bps"] = int(nif[1]) - lv
                netif["rx_bps"] = 8*int(netif["rx_bps"])
            else:
                netif["rx_bps"] = -1
        # TX Bytes per sec
            lv = int(getlastVal(nif[0], "tx_b"))
            if lv != -1:
                netif["tx_bps"] = int(nif[9]) - lv
                netif["tx_bps"] = 8*int(netif["tx_bps"])
            else:
                netif["tx_bps"] = -1
            netif["rx_MB"] = round(int(nif[1])/1000000.0, 2)
            netif["tx_MB"] = round(int(nif[9])/1000000.0, 2)
            tmp = getdebit(nif[0])
            netif["in KB/s"] = tmp[0]
            netif["out KB/s"] = tmp[1]
            netifs.append(netif)
            prv_mon_data.update({netif["interface"]: netif})
    else:
        p = subprocess.Popen('cat /proc/net/dev ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines = p.stdout.readlines()
        print " hahowa "
        # print prv_mon_data
        netifs = []
        count = 0
        for line in lines:
            count += 1
            if count < 3:
                continue
            nif = line.split()
            netif = OrderedDict()
            nif[0] = (nif[0].decode("utf-8")).replace(':', '')
            netif["interface"] = nif[0]
            netif["rx_b"] = int(nif[1])
            netif["tx_b"] = int(nif[9])
            netif["rx_pks"] = int(nif[2])
            netif["tx_pks"] = int(nif[10])
            netif["rx_error"] = int(nif[3])
            netif["rx_drops"] = int(nif[4])
            netif["tx_error"] = int(nif[11])
            netif["tx_drops"] = int(nif[12])
        # RX pkts per sec
            lv = int(getlastVal(nif[0], "rx_pks"))
            if lv != -1:
                netif["rx_pps"] = int(nif[2]) - lv
            else:
                netif["rx_pps"] = -1
        # TX pkts per sec
            lv = int(getlastVal(nif[0], "tx_pks"))
            if lv != -1:
                netif["tx_pps"] = int(nif[10]) - lv
            else:
                netif["tx_pps"] = -1
        # RX Bytes per sec
            lv = int(getlastVal(nif[0], "rx_b"))
            if lv != -1:
                netif["rx_bps"] = int(nif[1]) - lv
                netif["rx_bps"] = 8*int(netif["rx_bps"])
            else:
                netif["rx_bps"] = -1
        # TX Bytes per sec
            lv = int(getlastVal(nif[0], "tx_b"))
            if lv != -1:
                netif["tx_bps"] = int(nif[9]) - lv
                netif["tx_bps"] = 8*int(netif["tx_bps"])
            else:
                netif["tx_bps"] = -1
            netif["rx_MB"] = round(int(nif[1])/1000000.0, 2)
            netif["tx_MB"] = round(int(nif[9])/1000000.0, 2)
            tmp = getdebit(nif[0])
            netif["in KB/s"] = round(tmp[0])
            netif["out KB/s"] = round(tmp[1])
            netifs.append(netif)
            prv_mon_data.update({netif["interface"]: netif})
        netifs.append(getconnections())
    return netifs


def getlastVal(inter, mtric):
    if inter in prv_mon_data:
        return int(prv_mon_data[inter][mtric])
    else:
        return -1


def getdebit(name):

    debit = []
    p = subprocess.Popen('ifstat -i ' + name + ' 1 1 ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = p.stdout.readlines()
    db = lines[2].split()
    debit.append(float(db[0].rstrip()))
    debit.append(float(db[1].rstrip()))
    return debit


def getwrrd(name_int):
    debit = []
    tmp = (name_int.strip()).split("/dev/")
    name = filter(None, tmp)
    p = subprocess.Popen('iostat ' + name[0] + ' | grep ' + name[0], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = p.stdout.readlines()
    try:
        return lines[0].rstrip().split()
    except:
        return 6*[0]


def getconnections():
    p = subprocess.Popen('lsof -i | awk \'{print  $8,$9}\'|grep -v NAME', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = p.stdout.readlines()
    tmp_key = []
    cnx = OrderedDict({'TCP': {}, 'UDP': {}})
    for i in range(len(lines)):
        k = lines[i].split(":")
        if k[0][:3] in cnx.keys():
            if k[-1].rstrip() in tmp_key:
                cnx[k[0][:3]][k[-1].rstrip()]["nbr"] = cnx[k[0][:3]][k[-1].rstrip()]["nbr"]+1
                cnx[k[0][:3]][k[-1].rstrip()]["connections"].append((lines[i].split(" "))[1].rstrip())
            else:
                tmp_key.append(k[-1].rstrip())
                cnx[k[0][:3]][k[-1].rstrip()] = OrderedDict({"nbr": 1, "connections": [(lines[i].split(" "))[1].rstrip()]})

        else:
            tmp_key.append(k[-1].rstrip())
            cnx[k[0][:3]][k[-1].rstrip()] = OrderedDict({"nbr": 1, "connections": [(lines[i].split(" "))[1].rstrip()]})

    return {"opened connections": cnx}


def update(name, op):
    line = []
    with open("api/endpoint/vm.py") as f:
        line = f.readlines()
    if op == "ENABLE":
        find = "#@ns.route('/" + name
        for l in range(len(line)):
            if find in line[l]:
                line[l] = line[l][1:]
                print line[l][1:]

    elif op == "DISABLE":
        find = "@ns.route('/" + name
        for l in range(len(line)):
            if find in line[l]:
                line[l] = "#"+line[l]

    with open("api/endpoint/vm.py", 'w') as f:
        for item in line:
            f.write(item)


def update_agent_vm(desc={}):
    line = []
    with open(str(os.getcwd())+"/agent/api/builder/agent/api/endpoint/vm.py") as f:
        line = f.readlines()
    for find in desc["enable"]:
        print find
        find = "# @ns.route('/"+find
        for l in range(len(line)):
            if find in line[l]:
                line[l] = line[l][2:]

    for find in desc["disable"]:
        find = "@ns.route('/"+find
        for l in range(len(line)):
            if find in line[l]:
                if "#" in line[l]:
                    pass
                else:
                    line[l] = "# "+line[l]

    with open(str(os.getcwd())+"/agent/api/builder/agent/api/endpoint/vm.py", 'w') as f:
        for item in line:
            f.write(str(item))

        update_contraint(desc)
        return 204

    return 202


def update_contraint(desc={}):
    print desc
    config.set('host', 'username', desc["host"]["username"])
    config.set('host', 'password',  desc["host"]["password"])
    config.set('server',"server_ip", desc["host"]["server ip"])
    config.set('server',"server_port", desc["host"]["server port"])
    if config.get("agent","type")=="passive":
        config.set('contrainte', 'mem', desc["contraint"]["mem"])
        #config.set('contrainte', 'disk', info["agent contrainte"]["disk"])
        config.set('contrainte', 'cpu', desc["contraint"]["cpu"])
        with open(str(os.getcwd())+"/agent/api/builder/agent/config.conf", 'w') as set:
                config.write(set)
