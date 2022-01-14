#!/usr/bin/python3

import os
import stat
import argparse

from main.psu.QJ3005P import PSU

if __name__ == "__main__":

    if os.geteuid() != 0:
        exit("Check for root privileges failed... Try with 'sudo'")    

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--on', required=False, help='Switch UPS On', dest='on', action='store_true')
    group.add_argument('--off', required=False, help='Switch UPS Off',dest='off', action='store_true')
    parser.add_argument('-d', '--device', type=str, required=True, help='UPS tty device') 
    args = parser.parse_args()
    
    try: 
        mode = os.stat(args.device).st_mode
        if not stat.S_ISCHR(mode):
           exit(f'{args.device} is not a character device') 

        with PSU(args.device) as psu:
            if psu.is_available():
                print(f'Connected to PSU: {psu.name}, status: {psu.status}')
                if args.on:
            	    print('Switched ON')
            	    psu.enable()
                elif args.off:	
	                print('Switched OFF')
       		        psu.disable()
            else:
        	    print('PSU not found.')
        	    
    except FileNotFoundError as error:
        exit(f'{args.device} not found')

