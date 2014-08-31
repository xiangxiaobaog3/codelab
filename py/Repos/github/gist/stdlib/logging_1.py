# encoding: utf-8

# logging to a file

import logging

LOG_FILENAME = "logging_example.out"

logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

logging.debug("This message should go to the log file")

with open(LOG_FILENAME, 'rt') as fb:
    print "FILE:"
    print fb.read()


# Rotating Log Files

import glob
import logging.handlers

LOG_FILENAME = 'logging_rotatingfile_example.out'

# Set up a specific logger with our desired output level
my_logger = logging.getLogger("MyLogger")
my_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20, backupCount=5)

my_logger.addHandler(handler)

# Log some messages
for i in range(20):
    my_logger.debug("i = %d" % i)

print glob.glob("%s*" % LOG_FILENAME)
