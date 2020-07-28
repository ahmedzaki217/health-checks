#!/usr/bin/env python3.8
import os
import sys
import shutil
        
def check_reboot():
    """Returns true if vm has pending rebooted"""
    return os.path.exists("/run/reboot-required")


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

def check_root_full():
    """Returns true if root partition is full"""
    return check_disk_full(disk="/", min_gb = 2, min_percent = 10)
    
def main():
    checks=[(check_reboot, "Pending Reboot"), (check_root_full, "root partition is full.")]
    for check, msg in checks:
        if check():
            print(msg)
            sys.exit(1)
    print("Everything ok.")
    sys.exit(0)
main()
