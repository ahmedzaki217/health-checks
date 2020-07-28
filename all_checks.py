#!/usr/bin/env python3.8
import os
import sys
        
def check_reboot():
    """Returns true if vm has pending rebooted"""
    return os.path.exists("/run/reboot-required")

def main():
    if check_reboot():
        print("Pending Reboot.")
        sys.exit(1)
    print("Everything ok.")
    sys.exit(0)
main()
