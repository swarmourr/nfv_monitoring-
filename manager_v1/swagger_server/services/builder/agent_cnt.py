#--------------------------------------------------------#
# __developper__  = "hamza safri"                        #
# __code_objectif__= "monitoring container  consumption" #
# __language__    == "PYTHON  3"                         #
# __github__ == "Swarmourr"                              #
#--------------------------------------------------------#

import os
import time
import shlex
import subprocess
from collections import OrderedDict

mem_stat = {}
mem_limi = {}
mem_total = {}

"""
get generalinformation about the container
    uptime 
    ID
    DISTRIBUTION
    HOSTNAME 

"""
def info_cnt():
    infos = {}
    p = subprocess.Popen(('cat /proc/self/cgroup|grep :mem |cut -d/ -f3'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = p.stdout.readlines()
    p1 = subprocess.Popen(('cat /etc/*-release'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines1 = p1.stdout.readlines()
    p2 = subprocess.Popen(('uptime -p'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines2 = ' '.join(p2.stdout.readlines()[0].split())[2:]
    infos["uptime"] = lines2
    infos["container ID "] = lines[0].rstrip()
    infos["Distribution name "] = (lines1[0].split("="))[1].rstrip()
    infos["Distribution description "] = ((lines1[5].split("="))[1].rstrip()).replace('"', '')
    infos["Distribution release "] = ((lines1[9].split("="))[1].rstrip()).replace('"', '')
    infos["hostname"] = subprocess.Popen(('hostname'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()[0].strip()
    return infos

"""
get MEMORY consumption container

"""
def mem_cnt():
    mem = OrderedDict()
    swap = 0
    with open("/sys/fs/cgroup/memory/memory.stat", "r") as f:
        for line in f:
            (key, val) = line.split()
            mem_stat[key] = int(val)

    with open("/sys/fs/cgroup/memory/memory.limit_in_bytes") as f:
        mem_limi["limite"] = int(f.read())

    with open("/sys/fs/cgroup/memory/memory.usage_in_bytes") as f:
        mem_limi["usage"] = float(f.read())

    with open("/proc/meminfo", "r") as f:
        for line in f.readlines():
            tokens = line.split()
            if tokens[0] == 'MemTotal:':
                mem_total["total"] = (float(tokens[1]))
            break
        if "swap" in mem_stat:
            swap = mem_stat["swap"]
    mem["usage MiB"] = (mem_limi["usage"]-mem_stat["cache"])/(1.049e+6)
    mem["limite MiB"] = (mem_total["total"]/1048.576)
    mem["Swap"] = swap
    mem["consumption"] = round(((((mem_limi["usage"]-mem_stat["cache"])/(1.074e+6))/(mem_total["total"]/1048.576))*100), 9)

    return mem

"""
get CPU consumption container

"""
def cpu():
    with open("/proc/stat", "r") as f1:
        total_jeffies = None
        cpu_count = 0
        for l in f1.readlines():
            tokens1 = l.split()
            if tokens1[0] == 'cpu':
                if len(tokens1) < 8:
                    raise Exception("invalid")
                total_jeffies = sum(map(lambda t: int(t), tokens1[1:8]))

            elif tokens1[0].startswith('cpu'):
                cpu_count += 1
        cpu_time = (total_jeffies/os.sysconf(os.sysconf_names['SC_CLK_TCK']))*1e9
    return cpu_time, cpu_count


def c_cpu():
    with open("/sys/fs/cgroup/cpuacct/cpuacct.usage", "r") as f:
        return int(f.read())


def net_rx(name):
    with open("/sys/class/net/"+name+"/statistics/rx_packets", "r") as f:
        return int(f.read())


def net_rx_byte(name):
    with open("/sys/class/net/"+name+"/statistics/rx_bytes", "r") as f:
        return int(f.read())


def net_tx(name):
    with open("/sys/class/net/"+name+"/statistics/tx_packets", "r") as f:
        return int(f.read())


def net_tx_byte(name):
    with open("/sys/class/net/"+name+"/statistics/tx_bytes", "r") as f:
        return int(f.read())


def net_tx_dropped(name):
    with open("/sys/class/net/"+name+"/statistics/tx_dropped", "r") as f:
        return int(f.read())


def net_rx_dropped(name):
    with open("/sys/class/net/"+name+"/statistics/rx_dropped", "r") as f:
        return int(f.read())


def net_rx_errors(name):
    with open("/sys/class/net/"+name+"/statistics/rx_errors", "r") as f:
        return int(f.read())


def net_tx_errors(name):
    with open("/sys/class/net/"+name+"/statistics/tx_errors", "r") as f:
        return int(f.read())

"""
get NETWORK informations of container

"""
def net_i_o():
    p = subprocess.Popen(('ls /sys/class/net/'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = p.stdout.readlines()
    tmp = lines[0].split()
    stat = OrderedDict()
    for l in tmp:
        net = OrderedDict()
        net["rx_bytes"] = net_rx_byte(l)
        net["tx_bytes"] = net_tx_byte(l)
        net["rx_bytes_dropped"] = net_rx_dropped(l)
        net["tx_bytes_dropped"] = net_tx_dropped(l)
        net["rx_bytes_errors"] = net_rx_errors(l)
        net["tx_bytes_errors"] = net_tx_errors(l)
        # net["rx"]=net_rx_byte(l)+net_rx_dropped(l)+net_rx_errors(l)
        # net["tx"]=net_tx_byte(l)+net_tx_dropped(l)+net_tx_errors(l)
        net["debit"] = getdebit(l)
        stat[l] = net
    return stat


def getdebit(name):
    debit = {}
    p = subprocess.Popen('ifstat -i ' + name + ' 1 1 ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = p.stdout.readlines()
    db = lines[2].split()
    debit["in kB/s"] = float(db[0].rstrip())
    debit["out kB/s"] = float(db[1].rstrip())
    return debit


def blkio():
    metrics = {"read": 0, "write": 0}
    stats = []
    with open("/sys/fs/cgroup/blkio/blkio.throttle.io_service_bytes", "r") as f:
        stats = f.readlines()
    for line in stats:
        if "Read" in line:
            metrics["read MB"] = (int(line.split()[2])*2)/1e6
        if "Write" in line:
            metrics["write MB "] = int(line.split()[2])*2/1e6
    return metrics

"""
get disk information container

"""
def disk_cnt():
    all = []
    p = subprocess.Popen(('df -h | grep -vE \'^Filesystem|shm|boot\' | tr -s " "'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = p.stdout.readlines()
    for i in range(len(lines)):
        disk_info = OrderedDict()
        tmp = lines[i].split()
        disk = getwrrd_cnt(tmp[0])
        disk_info["Filesystem"] = tmp[0]
        disk_info["Size"] = tmp[1]
        disk_info["Used"] = tmp[2]
        disk_info["Available"] = tmp[3]
        disk_info["use %"] = tmp[4].rstrip("%")
        disk_info["Mount"] = tmp[5]
        disk_info["tps"] = disk[1]
        disk_info["read KB/s"] = disk[2]
        disk_info["write KB/s"] = disk[3]
        disk_info["read KB"] = disk[4]
        disk_info["write KB"] = disk[5]
        all.append(disk_info)
    return all


def cpu_c():
    s = cpu()
    c_s = c_cpu()
    rx_all = net_i_o()
    time.sleep(1)
    s1 = cpu()
    c_s1 = c_cpu()
    cpu_prct = (((c_s1-c_s)/(s1[0]-s[0]))/s[1])*100
    return {"cpu": cpu_prct}


def getwrrd_cnt(name_int):
    debit = []
    tmp = (name_int.strip()).split("/dev/")
    name = filter(None, tmp)
    p = subprocess.Popen('iostat ' + name[0] + ' | grep ' + name[0], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = p.stdout.readlines()
    try:
        return lines[0].rstrip().split()
    except:
        return 6*[0]

"""
get all connections established by the container

"""

def getconnections():
    p = subprocess.Popen('lsof -i | awk \'{print  $8,$9}\'|grep -v NAME', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = p.stdout.readlines()
    tmp_key = []
    cnx = OrderedDict({'TCP': {}, 'UDP': {}})
    for i in range(len(lines)):
        k = lines[i].split(":")
        if k[0][:3] in cnx.keys():
            if k[-1].rstrip() in tmp_key:
                if (lines[i].split(" "))[1].rstrip() in cnx[k[0][:3]][k[-1].rstrip()]["connections"]:
                    pass
                else:
                    cnx[k[0][:3]][k[-1].rstrip()]["nbr"] = cnx[k[0][:3]][k[-1].rstrip()]["nbr"]+1
                    cnx[k[0][:3]][k[-1].rstrip()]["connections"].append((lines[i].split(" "))[1].rstrip())
            else:
                tmp_key.append(k[-1].rstrip())
                cnx[k[0][:3]][k[-1].rstrip()] = OrderedDict({"nbr": 1, "connections": [(lines[i].split(" "))[1].rstrip()]})

        else:
            tmp_key.append(k[-1].rstrip())
            cnx[k[0][:3]][k[-1].rstrip()] = OrderedDict({"nbr": 1, "connections": [(lines[i].split(" "))[1].rstrip()]})

    return {"opened connections": cnx}

"""
get all information about the agent deployed in  the container

"""
def agent_info():
    ps = OrderedDict()
    p = subprocess.Popen('ps aux |grep \"python app.py\" | grep -v grep | tr -s \" \"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = p.stdout.readlines()
    tmp = lines[0].split()
    for i in range(len(tmp)):
        ps["PID"] = tmp[1]
        ps["CPU"] = tmp[2]
        ps["MEM"] = tmp[3]
        ps["State"] = tmp[7]
    return ps


"""
update the configuration of agents
"""

def update(name, op):
    line = []
    if name != "net":
        find = "@ns1.route('/" + name
    else:
        find = "@ns2.route('/" + name

    with open("api/endpoint/cnt.py") as f:
        line = f.readlines()
    if op == "ENABLE":
        find = "#"+find
        
        for l in range(len(line)):
            if find in line[l]:
                line[l] = line[l][1:]
    

    elif op == "DISABLE":
        for l in range(len(line)):
            if find in line[l]:
                line[l] = "#"+line[l]

    with open("api/endpoint/cnt.py", 'w') as f:
        for item in line:
            f.write(item)
        return 204

    return 202
