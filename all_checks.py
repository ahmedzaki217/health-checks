#!/usr/bin/env python3.8
import os
import sys
import shutil
        
def check_reboot():
    """Returns true if vm has pending rebooted"""
    return os.path.exists("/run/reboot-required")

def check_disk_full(disk, min_abs, min_percent):
    """Retruns true if there is not enaugh disk space other wise false"""
    du = shutil.disk_usage(disk)
    #calculate the percentage of free space
    percent_free = 100 * du.free / du.total
    #calculate how many gigabytes free
    gigabytes_free = du.free / 2**30
    
    if percent_free < min_percent or gigabytes_free < min_abs:
        return True
    return False

def main():
    if check_reboot():
        print("Pending Reboot.")
        sys.exit(1)
    if check_disk_full("/", 2, 10):
        print("Disk is full.")
        sys.exit(1)
    print("Everything ok.")
    sys.exit(0)
main()
