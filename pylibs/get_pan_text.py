from SimpleCV import Image
import sys
import time
import pytesseract
import re
import json

def learn_text(context, img_text):
    text_list = filter(lambda x: len(x) > 5, img_text.split('\n'))
    text_list = map(lambda x: re.sub(r'[\s]+', ' ', re.sub(r'[^A-Zl\d\/\s]+', '', x)).strip(), text_list)
    if 'best_list' not in context:
        context['best_list'] = text_list
    else:
        c_list = context['best_list']
        for i in xrange( min(len(c_list), len(text_list)) ):
            if len(text_list[i]) > len(c_list[i]):
                #print "%s => %s" % (c_list[i], text_list[i])
                c_list[i] = text_list[i]
            else:
                #print "%s <=> %s" % (c_list[i], text_list[i])
                pass

def get_fields(best_list):
    ret = {}
    idx = len(best_list) - 1
    pan = None
    while pan == None and idx > 1:
        cur_str = re.sub(r'[\s]', '', best_list[idx])
        if len(cur_str) == 10 and re.match(r'[A-Z]{5}[\d]{4}[A-Z]', cur_str):
            pan = cur_str
        idx -= 1

    if pan == None:
        idx = len(best_list) - 1
        ret['pan'] = {
                'val': best_list[idx],
                'confidence': 0
                }
    else:
        ret['pan'] = {
                'val': pan,
                'confidence': 100
                }

    dob = None
    while dob == None and idx > 1:
        cur_str = re.sub(r'[^\d]+', '', best_list[idx])
        if len(cur_str) > 5:
            dob = cur_str[:2] + '/' + cur_str[2:4] + '/' + cur_str[-4:]
        idx -= 1

    if dob == None:
        idx = len(best_list) - 2
        ret['dob'] = {
                'val': '',
                'confidence': 0
                }
    else:
        ret['dob'] = {
                'val': dob,
                'confidence': 100
                }

    father_name = None
    while father_name == None and idx > 0:
        cur_str = best_list[idx]
        if len( re.sub(r'[\s]+', '', cur_str) ) > 6:
            father_name = cur_str
        idx -= 1

    if father_name == None:
        idx = len(best_list) - 3
        ret['father_name'] = {
                'val': '',
                'confidence': 0
                }
    else:
        ret['father_name'] = {
                'val': father_name,
                'confidence': 60
                }

    name = None
    while name == None and idx >= 0:
        cur_str = best_list[idx]
        if len( re.sub(r'[\s]+', '', cur_str) ) > 6:
            name = cur_str
        idx -= 1

    if name == None:
        ret['name'] = {
                'val': '',
                'confidence': 0
                }
    else:
        ret['name'] = {
                'val': name,
                'confidence': 60
                }

    return ret


def get_pan_info(img_path):
    if img_path == None:
        img_path = sys.argv[1]
    print "Reading from file: " + img_path
    img = Image(img_path).toRGB()

    min_pan_area = img.width*img.height/10
    pan_rects = img.invert().findBlobs((25,0,0), min_pan_area)

    if pan_rects and len(pan_rects) > 0:
        img = img.crop(pan_rects[0])

    if img.width < 350 or img.height < 200:
        print "Error too small PAN image"
        exit(1)

    cropped_img = img.crop(0, img.height/4.60, img.width/1.4, img.height/4*2.3)
    if cropped_img.width < 550:
        cropped_img = cropped_img.resize(550, 550*cropped_img.height/cropped_img.width)

    t_img = cropped_img.threshold(100)
    img_text = pytesseract.image_to_string(t_img.getPIL(), lang='eng')
    context = {}
    learn_text(context, img_text)

    t_img = cropped_img
    img_text = pytesseract.image_to_string(t_img.getPIL(), lang='eng')
    learn_text(context, img_text)

    t_img = cropped_img.threshold(90)
    img_text = pytesseract.image_to_string(t_img.getPIL(), lang='eng')
    learn_text(context, img_text)

    t_img = cropped_img.threshold(110)
    img_text = pytesseract.image_to_string(t_img.getPIL(), lang='eng')
    learn_text(context, img_text)

    #print context['best_list']
    pan_info = get_fields(context['best_list'])
    #print json.dumps(pan_info, indent=2)
    return pan_info

    #cropped_img.show()
    #time.sleep(3)

