#!/usr/bin/python

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#-----CONSTANTS
HOST=           'localhost'
DBUSER=         'mysqlusername'
DBPASS=         'mysqlpassword'
DBNAME=         'mysqldatabasename'

KEY_ESIT=       'esit'
KEY_RESULT=     'result'
KEY_CMD=        'cmd'

GOOGLE_API_KEY=	'AIzaSyBGg-A5iwi5jEDX_G44ekc0uBgUJ-6j8Rk'
ESPN_API_KEY=	'ufuancvzf7xb58f9zh7khr32'
#db=MySQLdb.connect(HOST,DBUSER,DBPASS,DBNAME)

FILE_DEFAULTS_URL=      '/media/hd2/sportapp/sportappdefaults.xml'

BASE_URL=               "http://162.216.4.195"
UPLOAD_IMAGE_URL=       "http://162.216.4.195/sex/img/profilepic/images/"
BASE_PICTURE_DIR=       "/media/hd2/sportapp/img/profilepic/"
UPLOAD_IMAGE_DIR=       "images/"
UPLOAD_THUMB_DIR=       "images/thumb/"
DEFAULTNOIMAGE_PATH=	"/media/hd2/sportapp/defaultthumb.png"

ESIT_OK=		0
ESIT_ERROR=		2
ESIT_EXIST=		1
ESIT_SECUTIRYFAULT=	-2

THUMB_PIC_W = 120 # this is the maximum width of the images
THUMB_PIC_H = 120 # this is the maximum height of the images
#ratio = 1. * THUMB_PIC_W / THUMB_PIC_H
