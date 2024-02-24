# !/usr/bin/python
# from io import StringIO
from StringIO import StringIO
import base64
# from base64 import decodestring
import random
import string
from utility import ErrorLog, id_generator
from PIL import Image
import urllib
import urllib2
import json

DEFAULTNOIMAGE_PATH = "/media/hd2/sportapp/defaultthumb.png"
DEFAULT_LOGO_PATH = "/media/hd2/sportapp/powered-by-espn-silver_200.png"

# --------------------------------------------------------------------
def Base64FromUrl(url):
    """
    returns the base64 string of the image from the passed url
    :param url:     the url of the image
    :return:        the base64 string of the image
    """
    return base64.b64encode(urllib.urlopen(url).read())


#--------------------------------------------------------------------
def CropResizeImg(origFilePath, destFilePath, img_w, img_h):
    """
    crops and resize the image to create the thumbnail
    :param origFilePath:    the path of the file on the disc
    :param destFilePath:    the destination file path on the disc
    :param img_w:           the desired image width
    :param img_h:           the desired image height
    """

    ratio = 1. * img_w / img_h
    im = Image.open(origFilePath)  # open the input file
    im = resize(im, img_w, img_h)
    #im.save(fout, "jpeg", quality = 100) # save the image
    #fout.close()
    im.save(destFilePath)


#--------------------------------------------------------------------
def CropResizeImg64(orig64, img_w, img_h):
    """
    crops and resize the image to create the thumbnail from a base64 string
    :param orig64: the base64 string of the image
    :param img_w:  the desired image width
    :param img_h:  the desired image height
    :return:       the resized/cropped base64 string of the image
    """
    ratio = 1. * img_w / img_h
    #if isinstance(orig64, str):
    #	orig64 = StringIO(orig64)
    #im = Image.open(orig64)
    #image = Image.fromstring('RGB',(width,height),decodestring(orig64))
    #im = Image.open(StringIO(base64.b64decode(orig64))) # open the input file

    #image = open("/media/hd2/sportapp/imagetempthumb.png", "wb")
    #image.write(base64.b64decode(orig64))#.decode('base64'))
    #image.close()
    #im = Image.open("/media/hd2/sportapp/imagetempthumb.png")
    im = Image.open(StringIO(base64.b64decode(orig64)))
    im = resize(im, img_w, img_h)
    buf = StringIO()
    im.save(buf, format='PNG')
    jpeg = buf.getvalue()
    return base64.b64encode(jpeg)


#--------------------------------------------------------------------
def CropResizeImg64Save(orig64, img_w, img_h, dest):
    """
    crops and resize the image to create the thumbnail from a base64 string
    and saves it to disc
    :param orig64: the base64 string of the image
    :param img_w:  the desired image width
    :param img_h:  the desired image height
    :param dest:   the destination file path on the disc
    """
    dest64 = CropResizeImg64(orig64, img_w, img_h)
    im = Image.open(StringIO(base64.b64decode(dest64)))
    im.save(dest)


#savepath="/media/hd2/sportapp/pic_temp/%s.png"% id_generator(7)
#result64=''
#try:
#	im.save(savepath)
#	with open(savepath, "rb") as image_file:
#		result64 = base64.b64encode(image_file.read())
#	#im.save(fout, "jpeg", quality = 100) # save the image
#	#fout.close()
#except:
#	with open(DEFAULTNOIMAGE_PATH, "rb") as image_file:
#                result64 = base64.b64encode(image_file.read())
#return result64


def ResizeImg64(orig64, basesize=900, qualityJpg=70):
    """
    resize a base64 image without cropping
    :param orig64:      the base64 string of the image
    :param basesize:    the desired size of the base of the resulting image
    :param qualityJpg:  values from 1 to 100, the desired resulting image quality
    :return:            the resized base64 string of the image
    """
    #ratio = 1. * img_w /img_h
    im = Image.open(StringIO(base64.b64decode(orig64)))
    (width, height) = im.size  # get the size of the input image
    if width < basesize: basesize = width

    im = im.resize((basesize, height / (width / basesize)), Image.BICUBIC)  #ANTIALIAS,BICUBIC,BILINEAR,NEAREST

    #convert the image to RGB
    if im.mode != "RGB":
        im = im.convert("RGB")

    buf = StringIO()
    try:
        im.save(buf, "JPEG", quality=qualityJpg, optimize=True, progressive=True)
    except Exception, d:
        try:
            ErrorLog("ResizeImg64 error, saving no optimization: %s" % d)
            im.save(buf, "JPEG", quality=qualityJpg - 10)
        except Exception, dfg:
            try:
                ErrorLog("ResizeImg64 error, saving uncompressed: %s" % dfg)
                im.save(buf, format='JPEG')
            except Exception, k:
                ErrorLog("ResizeImg64 INNER error,saving png: %s" % k)
                im.save(buf, format='PNG')
    jpeg = buf.getvalue()
    return base64.b64encode(jpeg)

#--------------------------------------------------------------------
def BlendEspnLogo(orig64, logoPath=DEFAULT_LOGO_PATH):
    #orig64=JpgToPng64(orig64)
    im = Image.open(StringIO(base64.b64decode(orig64)))
    im2 = Image.open(logoPath)
    (width, height) = im.size
    basesize = width / 7
    im2 = im2.resize((basesize, height / (width / basesize)), Image.BICUBIC)
    im.paste(im2, ((width - basesize) - 5, (height - (height / (width / basesize))) - 5))
    buf = StringIO()
    try:
        im.save(buf, format='JPEG')
    except Exception, k:
        ErrorLog("BlendLogo error,saving png: %s" % k)
        im.save(buf, format='PNG')
    jpeg = buf.getvalue()
    return base64.b64encode(jpeg)


#--------------------------------------------------------------------
def JpgToPng64(orig64):
    im = Image.open(StringIO(base64.b64decode(orig64)))
    buf = StringIO()
    im.save(buf, format='PNG')
    jpeg = buf.getvalue()
    return base64.b64encode(jpeg)


#--------------------------------------------------------------------
def resize(im, img_w, img_h):
	"""
	function to resize the Image to desired width and height
	:param im:
	:param img_w:
	:param img_h:
	:return:
	"""
	
	ratio = 1. * ((img_w * 1.)/(img_h * 1.))
	(width, height) = im.size  # get the size of the input image
	#print "ratio %s %s %s"%(ratio,width, height)

	top = 0
	bottom = height
	left = 0
	right = width
    
	if width > height * ratio:
		# crop the image on the left and right side
		newwidth = ((height * 1.) * ratio)
		left2 =((width * 1.) / 2 - newwidth / 2)
		left = (int) (left2 * 1)
		right =(int) (left2 + newwidth)
		# keep the height of the image
		#top = 0
		#bottom = height
	elif width < height * ratio:
      	# crop the image on the top and bottom
		newheight = ((width * 1.) / ratio)
		top2 =((height * 1.) / 2 - newheight / 2)
		top =(int) (top2 * 1)
		if(top<0):top=top * -1
		bottom = (int)(top2 + newheight)
		# keep the width of the impage
        #left = 0
        #right = width
		
	if width != (height * ratio):
		#print "lets crop , left:%s top:%s right:%s bottom:%s height:%s"%(left, top, right, bottom,height)
		im = im.crop((left, top,right,bottom))

    #assert isinstance(im, object)
	return im.resize((img_w, img_h), Image.BICUBIC)  #ANTIALIAS,BICUBIC,BILINEAR,NEAREST
