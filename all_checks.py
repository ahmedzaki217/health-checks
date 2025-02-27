#!/usr/bin/env python3.8
import os
import sys
import shutil
import psutil
import socket
from memory_profiler import profile
@profile        
def check_reboot():
    """Returns true if vm has pending rebooted"""
    return os.path.exists("/run/reboot-required")

@profile
def check_disk_full(disk, min_percent, min_gb):
    """Retruns true if there is not enaugh disk space other wise false"""
    du = shutil.disk_usage(disk)
    #calculate the percentage of free space
    percent_free = 100 * du.free / du.total
    #calculate how many gigabytes free
    gigabytes_free = du.free / 2**30
    
    if percent_free < min_percent or gigabytes_free < min_gb:
        return True
    return False
@profile
def check_root_full():
    """Returns true if root partition is full"""
    return check_disk_full(disk="/", min_gb = 2, min_percent = 10)

def check_cpu_constrained():
    """Return True if cpu have too much usage, false otherwise"""
    return psutil.cpu_percent(1) > 75
@profile    
def check_no_network():
    """Return True if it fails to resolve Google's URL, False otherwise"""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True
        
@profile            
def main():
    checks=[(check_reboot, "Pending Reboot"), (check_root_full, "root partition is full.")
    ,(check_no_network, "No working network."), (check_cpu_constrained, "CPU load is too high")]
    everything_ok = True
    for check, msg in checks:
        if check():
            print(msg)
            everything_ok = False
    if not everything_ok:
        sys.exit(1)
    print("Everything ok.")
    sys.exit(0)

main()
