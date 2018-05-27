import cv2
import numpy as np
from preprocessing import Prep as p
from featext.texture import Haralick as har
from featext.texture import Tamura as tam

obj = p.Prep('Melanoma.jpg')
print(obj.getArrayOfGrayLevelsWithFreq(obj.getSegGrayImg()))
feobj = har.HarFeat(obj.getSegGrayImg(), obj.getArrayOfGrayLevelsWithFreq(obj.getSegGrayImg()))
#feobj2 = tam.TamFeat(obj.getSegGrayImg())

def showColImg():
    cv2.namedWindow('imgcol', cv2.WINDOW_NORMAL)
    cv2.imshow('imgcol', obj.getActImg())
    cv2.waitKey(0)


def showGrayImg():
    cv2.namedWindow('imggray', cv2.WINDOW_NORMAL)
    cv2.imshow('imggray', obj.getGrayImg())
    cv2.waitKey(0)


def showInvertedGrayImg():
    cv2.namedWindow('imggrayinvrt', cv2.WINDOW_NORMAL)
    cv2.imshow('imggrayinvrt', obj.getInvrtGrayImg())
    cv2.waitKey(0)


def showBinImg():
    cv2.namedWindow('imgbin', cv2.WINDOW_NORMAL)
    cv2.imshow('imgbin', obj.getBinaryImg())
    cv2.waitKey(0)


def showSegmentedColorImg():
    cv2.namedWindow('segimgcol', cv2.WINDOW_NORMAL)
    cv2.imshow('segimgcol', obj.getSegColImg())
    cv2.waitKey(0)


def showSegmentedGrayImg():
    cv2.namedWindow('segimggray', cv2.WINDOW_NORMAL)
    cv2.imshow('segimggray', obj.getSegGrayImg())
    cv2.waitKey(0)

def showGLCM():
    print(np.sum(feobj.getGLCM()))
    print(feobj.getGLCM())

def showHaralickFeatures():
    print("Angular Second Moment-ASM of seg gray img %f \n" % feobj.getAngularSecondMomentASM())
    print("Energy of seg gray img %f \n" % feobj.getEnergy())
    print("Entropy of seg gray img %f \n" % feobj.getEntropy())
    print("Contrast of seg gray img %f \n" % feobj.getContrast())
    print("Homogeneity of seg gray img %f \n" % feobj.getHomogeneity())
    print("Directional-Moment of seg gray img %f \n" % feobj.getDm())
    print("Correlation of seg gray img %f \n" % feobj.getCorrelation())
    print("Haralick-Correlation of seg gray img %f \n" % feobj.getHarCorrelation())
    print("Cluster-Shade of seg gray img %f \n" % feobj.getClusterShade())
    print("Cluster-Prominence of seg gray img %f \n" % feobj.getClusterProminence())
    print("Moment1 of seg gray img %f \n" % feobj.getMoment1())
    print("Moment2 of seg gray img %f \n" % feobj.getMoment2())
    print("Moment3 of seg gray img %f \n" % feobj.getMoment3())
    print("Moment4 of seg gray img %f \n" % feobj.getMoment4())
    print("Differential-ASM of seg gray img %f \n" % feobj.getDasm())
    print("Differential-Mean of seg gray img %f \n" % feobj.getDmean())
    print("Differential-Entropy of seg gray img %f \n" % feobj.getDentropy())

"""def showTamuraFeatures():
    print("Coarseness of seg gray img %f \n" % feobj2.getCoarseness())"""

showColImg()
showGrayImg()
showInvertedGrayImg()
showBinImg()
showSegmentedColorImg()
showSegmentedGrayImg()
showGLCM()
showHaralickFeatures()
#showTamuraFeatures()



