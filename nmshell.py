#!/usr/bin/env python3
from importlib.util import find_spec

import os
import sys
import signal

nmap_mod_found = find_spec("nmap")
if not nmap_mod_found:
    print("""python-nmap for python 3 is not found but is required.

Package name : python3-nmap or python-nmap

Archlinux : pacman -S python-nmap
Debian : apt install python3-nmap

https://pypi.python.org/pypi/python-nmap""")
    
    sys.exit(1)

from console.Console import *

def signal_handler(signal, frame):
        print('Exit ...')
        sys.exit(0)

def start():
    c = Console()


if __name__ == '__main__':
    """
        run program
    """
    if(os.getuid() != 0):
        print("Nop, must be root")
        sys.exit(1)

    

    print("""
 _____________________________________ 
 
      < NmapShell v2.0 >
 Not sure what to do ? type 'help' 
        \   ^__^
         \  (oo)\_______
            (__)\       )\/o
                ||----w |
                ||     ||
""")
    signal.signal(signal.SIGINT, signal_handler)	
    start()
