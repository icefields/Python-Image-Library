#!/usr/bin/python

try:
    import MySQLdb
except ImportError, e:
	print "Import Error,exception: %s"%e
     
import json
import base64
import random
import string
import urllib2
import cgi
import cgitb
import datetime
import time
import xmltodict
import os.path

from defs import FILE_DEFAULTS_URL

ERRORLOG_PATH = '/media/hd2/sportapp/sportapp_log.txt'



# --------------------------------------------------------------------
# -----it generates a random string, useful for filenames
def id_generator(size=22, chars=string.ascii_uppercase + string.digits):
    dnow = TimeUtc(datetime.datetime.now())
    drand = ''.join(random.choice(chars) for x in range(size))
    return "%s%d" % (drand, dnow)


#--------------------------------------------------------------------
#-----extract the hash tag from a string
def ErrorLog(errormessage):
    er = ''
    try:
        f = open(ERRORLOG_PATH, 'a')
        dicty = {}
        dicty['date'] = "%s" % datetime.datetime.now()
        dicty['error'] = "%s" % errormessage
        f.write(json.dumps(dicty) + "\n")
        #f.write("date:%s\n%s\n\n"%(datetime.datetime.now(),"%s"%errormessage))
        f.close()
    except Exception, g:
        er = '1'


#--------------------------------------------------------------------
#-----it generates a random string, useful for filenames
def TimeUtc(timeD):
    if timeD is None: return 0.0
    return time.mktime(timeD.timetuple())
