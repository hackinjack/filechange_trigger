#!/usr/bin/env python
# <jack-f.knight@ubs.com>
# 20200702
#
# Quick n dirty script to watch a file for desired value inside and replace
# Usage:
#   filechange_trigger <file_to_watch> <expected_value> <desired_value>
# 
# e.g.
# Specific use case - monitor /proc/sys/net/ipv4/ip_forward for
# something like puppet changing it to 0 when I want it set to 1
#
#   filechange_trigger.py /proc/sys/net/ipv4/ip_forward 0 1
#
import pyinotify
import logging
import sys
import os
import signal

scriptname = os.path.basename(sys.argv[0])
#logfile = sys.stderr
#logfile = "/var/log/%s.log" % (scriptname)
logfile = "/tmp/%s.log" % (scriptname)

# set up logging with timestamp
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 
file_handler = logging.FileHandler(logfile)
formatter = logging.Formatter('%(asctime)s:%(levelname)-8s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#    datefmt='%Y%m%d:%H%M%S',
#    file=logfile)

def KeyboardInterruptHandler(signal, frame):
    logger.info("Exiting on keyboard interrupt %s" % (signal))
    sys.exit(0)

signal.signal(signal.SIGINT, KeyboardInterruptHandler)

wm = pyinotify.WatchManager()   # Watch Manager
mask = pyinotify.IN_MODIFY      # watched events

# check args
if len(sys.argv) != 4:
    usagemsg = "%s: Usage: <file_to_watch> <expected_value> <desired_value>" \
    % (os.path.basename(sys.argv[0]))
    logger.error(usagemsg)
    sys.exit(1)
    pass

logger.info("%s started. Watching %s for value %s, will replace with %s. Logging to %s"
    % (scriptname, sys.argv[1], sys.argv[2], sys.argv[3], logfile))


class EventHandler(pyinotify.ProcessEvent):
# Any time the file gets modded, check if it contains the trigger value
    def process_IN_MODIFY(self, event):
        try:
            f = open(event.pathname, "r+")
            fval = f.read()
            if int(fval) != 1:
                logger.info("Detected value %s in %s: writing %s" %(sys.argv[2], event.pathname, sys.argv[3]))
                f.seek(0)
                f.write(sys.argv[3])
                f.seek(0)
                logger.info("%s now contains value %s" % (event.pathname, f.read()))
                f.close()
        except IOError, e:
            logger.error("File operation error: %s" % (e))
        except Exception:
            raise

# check and set initial value
try:
    f = open(sys.argv[1], "r+")
    fval = f.read()
    if int(fval) != 1:
        logger.info("Detected value %s in %s: writing %s" %(sys.argv[2], sys.argv[1], sys.argv[3]))
        f.seek(0)
        f.write(sys.argv[3])
        f.seek(0)
        logger.info("%s now contains value %s" % (sys.argv[1], f.read()))
        f.close()
except IOError, e:
    logger.error("File operation error: %s" % (e))
except Exception:
    raise

# Now set the watch 
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('/tmp/text.txt', mask, rec=True)

notifier.loop()
