#!/usr/bin/env python
#
# This file is licensed under the terms of the GPL, Version 3
# 
# Copyright 2016 Dario Carluccio <check_owserver.at.carluccio.de>

__author__ = "Dario Carluccio"
__copyright__ = "Copyright (C) Dario Carluccio"
__license__ = "GPLv3"
__version__ = "1.0"

import os
import logging
import signal
import socket
import sys
import argparse
import ow

parser = argparse.ArgumentParser( formatter_class=argparse.RawDescriptionHelpFormatter,  
description='''connects to onewire-server and retrieves temperature from 
onewire sensor and check, if temperature exceeds the 
defined warning oder critical levels.''',  
epilog='''exit status:
  0 - OK:       sensor value is between defined ranges.
  1 - WARNING:  sensor value exceeds warning limits 
                but not critical limits.
  2 - CRITICAL: sensor value exceeds critical limits, 
                or sensor was not found.''')                                                               
parser.add_argument('sensor_id', metavar="<sensor_id>", help='ID of 1-wire sensor')
parser.add_argument('-cl', '--critical_low', metavar="<critical low>", dest='crit_low', type=int, help='critical low value (default -50)', default ='-50')
parser.add_argument('-ch', '--critical_high', metavar="<critical high>", dest='crit_high', type=int, help='critical high value (default 120)', default ='120')
parser.add_argument('-wl', '--warning_low', metavar="<warning low>", dest='warn_low', type=int, help='warning low value (default -50)', default ='-50')
parser.add_argument('-wh', '-warning_high', metavar="<warning high>", dest='warn_high', type=int, help='warning high value (default 120)', default ='120')
parser.add_argument('-s', '--server', metavar="<server>", dest='server', help='owserver address (::1)', default ='::1')
parser.add_argument('-p', '--port', metavar="<port>", dest='port', type=int, help='owserver port (default 4304)', default ='4304')
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()

# LOGFORMAT = '%(asctime)s - %(message)s'
LOGFORMAT = '%(message)s'

if args.verbose:
    logging.basicConfig(level=logging.DEBUG, format=LOGFORMAT)
    LOGLEVEL = "DEBUG"    
else:
    logging.basicConfig(level=logging.INFO,  format=LOGFORMAT)
    LOGLEVEL = "INFO"

def cleanup(signum, frame):
    """
    Signal handler to ensure we disconnect cleanly
    in the event of a SIGTERM or SIGINT.
    """
    logging.debug("Exiting on signal %d", signum)
    sys.exit(signum)

def main_loop():
    """
    main loop 
    """
    logging.debug(("ow.init (%s:%s)") % (args.server, args.port))
    ow.init(("%s:%s") % (args.server, args.port))
    ow.error_level(ow.error_level.fatal)
    ow.error_print(ow.error_print.stderr)
    logging.debug(("Querying %s") % (args.sensor_id))
    try:
        # Create sensor object
        sensor = ow.Sensor(args.sensor_id)
        # Query sensor state
        owtemp = float(sensor.temperature)
        logging.debug(("Sensor %s : %s") % (args.sensor_id, owtemp))
        
        # Check critical
        if owtemp < args.crit_low  or owtemp > args.crit_high:
            # CRITICAL - 24,58 C |temp=24,58;25:35;15:55;0;120 
            print (("CRITICAL - %.2f C|temp=%.2f;%s:%s;%s:%s") % (owtemp, owtemp , args.warn_low, args.warn_high, args.crit_low, args.crit_high))
            sys.exit(2) 
        elif owtemp < args.warn_low or owtemp > args.warn_high:
            # WARNING - 24,58 C |temp=24,58;25:35;15:55;0;120
            print (("WARNING - %.2f C|temp=%.2f;%s:%s;%s:%s") % (owtemp, owtemp , args.warn_low, args.warn_high, args.crit_low, args.crit_high))
            sys.exit(1)             
        else:            
            # OK - 24,58 C |temp=24,58;25:35;15:55;0;120
            print (("OK - %.2f C|temp=%.2f;%s:%s;%s:%s") % (owtemp, owtemp, args.warn_low, args.warn_high, args.crit_low, args.crit_high))
            sys.exit(0)
            
    except ow.exUnknownSensor:
        logging.info("CRITICAL - Sensor %s not found", args.sensor_id)
        print ("CRITICAL - Sensor %s not found" % args.sensor_id)
        sys.exit(3)

# Use the signal module to handle signals
signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

# start main loop
try:
    main_loop()
except KeyboardInterrupt:
    logging.info("Interrupted by keypress")
    sys.exit(0)            
    
