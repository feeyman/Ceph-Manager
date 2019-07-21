#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import json
import psutil
import commands
from prettytable import PrettyTable

def main():
    printosdcputable()

def printosdcputable():
    row = PrettyTable()
    row.header = True
    cpulist = ["OSD\CPU"]
    corelist=["Core ID"]
    phylist = ["Physical ID"]
    emplist=["-----------"]
    for cpupro in range(psutil.cpu_count()):
        cpulist.append("%s" %cpupro )

        coreid=commands.getoutput('egrep \'processor|physical id|core id\' /proc/cpuinfo | cut -d : -f 2 | paste - - -  | awk  \'$1==%s {print $3 }\'' %cpupro)
        corelist.append("%s" %coreid)

        phyid = commands.getoutput('egrep \'processor|physical id|core id\' /proc/cpuinfo | cut -d : -f 2 | paste - - -  | awk  \'$1==%s {print $2 }\'' % cpupro)
        phylist.append("%s" %phyid)
        emplist.append("--")

    row.field_names = cpulist
    row.add_row(corelist)
    row.add_row(phylist)
    row.add_row(emplist)

    for root, dirs, files in os.walk('/var/run/ceph/'):
        for name in files:
            if "osd"  in name and "pid" in name :
                osdlist = []
                for osdcpu in range(psutil.cpu_count()):
                    osdlist.append(" ")
                pidfile=root+ name
                osdid=commands.getoutput('ls  %s|cut -d "." -f 2 2>/dev/null'  %pidfile )
                osdpid = commands.getoutput('cat %s  2>/dev/null' %pidfile)
                osd_runcpu = commands.getoutput('ps -o  psr -p %s |grep -v PSR 2>/dev/null' %osdpid)
                osdname="osd."+osdid
                osdlist[int(osd_runcpu)]="+"
                osdlist.insert(0,osdname)
                row.add_row(osdlist)
    print row

if __name__ == '__main__':
    main()
