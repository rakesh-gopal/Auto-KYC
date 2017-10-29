import re
from pymongo import MongoClient
from pylibs.is_photoshopped import *
from pylibs.get_pan_text import get_pan_info
import time

client = MongoClient('localhost', 3001)
db = client['meteor']

def process_image(img):
    print "Processing Image: %s" % img['_id']
    fpath = str(img['path'])
    updates = {}
    is_shopped, confidence = is_photoshopped(fpath)
    if is_shopped:
        print "File is Photoshopped (Confidence: %d%%)" % confidence
    else:
        print "File is Genuine (Confidence: %d%%)" % confidence

    updates['is_photoshopped'] = is_shopped
    updates['is_photoshopped_confidence'] = confidence

    pan_info = get_pan_info(fpath)
    print pan_info
    updates['auto_vals'] = pan_info
    updates['is_processed'] = True
    db.images.update_one({'_id': img['_id']}, {'$set': updates})

while True:
    time.sleep(1)
    print "Looking for files..."
    new_images = db.images.find({
        'is_processed': False
        })
    for img in new_images:
        process_image(img)

