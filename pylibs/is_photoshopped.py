import sys
import urllib2
import numpy as np
import numpy.linalg as la
import matplotlib as mp
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
import SimpleCV
import warnings
import time
warnings.simplefilter(action='ignore', category=FutureWarning)

COLOR_DEV_THRESHOLD_PERCENT = 25

def contains_pan(img_path):
    if img_path == None:
        img_path = sys.argv[1]
    print "Reading from file: |" + img_path + "|"
    img = SimpleCV.Image(img_path).toRGB()
    min_pan_area = img.width*img.height/10
    pan_rects = img.invert().findBlobs((25,0,0), min_pan_area)
    if pan_rects and len(pan_rects) > 0:
        img = img.crop(pan_rects[0])
        pass

    LIFE = img.getNumpy()
    row_avg = np.average(LIFE, axis=0)
    avg = np.average(row_avg, axis=0)

    print "Color Avg: " + str(avg)
    color_deviation = abs(avg[1]-avg[0]-19) + abs(avg[2]-avg[1]-20) + abs(avg[2]-avg[0]-41)
    error_confidence = int( ((color_deviation**2)/256**2)**(0.5) *100)
    if error_confidence > COLOR_DEV_THRESHOLD_PERCENT:
        print "Could not detect PAN card. Please use better lighting and camera. (Confidence: %s%%)." % int(error_confidence*100.0/(100-COLOR_DEV_THRESHOLD_PERCENT))
        return False
    else:
        print "Detected valid PAN. (Confidence: %s%%)" % (100-error_confidence)
        return True


def is_photoshopped(img_path):
    if img_path == None:
        img_path = sys.argv[1]
    print "Reading from file: |" + img_path + "|"
    img = SimpleCV.Image(img_path).toRGB()
    min_pan_area = img.width*img.height/10
    pan_rects = img.invert().findBlobs((25,0,0), min_pan_area)
    if pan_rects and len(pan_rects) > 0:
        img = img.crop(pan_rects[0])
        pass

    LIFE = img.getNumpy()

    def photoshop_detector(img):
        rows, cols, colors = img.shape
        flattened = img.reshape((-1, colors)) # flatten rows and cols into a single dimension
        # PCA is just the SVD of the covariance matrix
        U, S, V = la.svd(np.cov(flattened.T))

        PC2 = U[:,1] # 2nd principle component
        projected = np.dot(flattened,PC2)
        return np.reshape( projected, (rows,cols)) # unflatten

    processed_im = photoshop_detector(LIFE);
    threshold = threshold_otsu(processed_im)
    print "Threshold: " + str(threshold)
    percentage = np.count_nonzero(processed_im>threshold) * 100.0/ np.count_nonzero(processed_im) 
    print percentage
    if (percentage<50.0):
        #print "Photoshopped : ", (100-percentage)
        return (True, (100-percentage))
    else:
        #print "Not photoshopped"
        return (False, (percentage))
    #plt.imshow(processed_im>threshold, cmap = mp.cm.Greys_r)
    #plt.show()

