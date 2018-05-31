import numpy as np
from util import Util as u
import cv2

class TamFeat(object):

    def __init__(self, img):
        self.__coarseness = self.__generateCoarseness(img)
        (self.__contrast, self.__kurtosis) = self.__generateContrastAndKurtosis(img)
        self.img_hor_x = cv2.filter2D(img, -1, np.array([[1,1,1],[0,0,0],[-1,-1,-1]], dtype=np.int16))
        self.img_vert_y = cv2.filter2D(img, -1, np.array([[-1,0,1],[-1,0,1],[-1,0,1]], dtype=np.int16))
        self.delg_img = np.round((np.add(self.img_hor_x, self.img_vert_y, dtype=float) * 0.5)).astype(np.int8)
        self.theta_img = np.tanh(np.divide((self.img_vert_y).astype(float), (self.img_hor_x).astype(float), dtype=float, out=np.zeros_like((self.img_vert_y).astype(float)), where=self.img_hor_x != 0)) + (float(np.pi) / 2.0)
        self.linelikeness = self.__generateLineLikeness(self.delg_img, self.theta_img)

    def __generateCoarseness(self, src_img):
        sbest = np.zeros(src_img.shape, np.uint32, 'C')
        for x in range(0, (src_img.shape)[0], 1):
            for y in range(0, (src_img.shape)[1], 1):
                emax = np.empty(0, np.dtype([('E', float), ('K', int)]), 'C')
                for k in range(1, 7, 1):
                    emax = np.insert(emax, emax.size, (np.abs(self.__nebAvg(x + np.float_power(2, k-1), y, k, src_img) - self.__nebAvg(x - np.float_power(2, k-1), y, k, src_img)), k-1), 0)
                    emax = np.insert(emax, emax.size, (np.abs(self.__nebAvg(x, y + np.float_power(2, k-1), k, src_img) - self.__nebAvg(x, y - np.float_power(2, k-1), k, src_img)), k-1), 0)
                emax.sort(axis=0, kind='mergesort', order='E')
                sbest[x, y] = np.float_power(2, (emax[emax.size-1])[1])
        return (float(np.sum(sbest, axis=None, dtype=float) / float(sbest.size)))

    def __nebAvg(self, x, y, k, src_img):
        avg = 0.0
        const = np.float_power(2, k-1)
        xh = int(np.round(x + const - 1))
        xl = int(np.round(x - const))
        yh = int(np.round(y + const - 1))
        yl = int(np.round(y - const))
        (xl, xh, yl, yh) = self.__checkSigns(xl, xh, yl, yh, src_img.shape)
        for r in range(xl, xh, 1):
            for c in range(yl, yh, 1):
                avg = avg + (float(src_img[r, c]) / float(np.float_power(2, 2*k)))
        return avg

    def __checkSigns(self, xl, xh, yl, yh, shape):
        if (xl < 0):
            xl = 0
        if (xl > shape[0]):
            xl = shape[0]
        if (xh < 0):
            xh = 0
        if (xh > shape[0]):
            xh = shape[0]
        if (yl < 0):
            yl = 0
        if (yl > shape[1]):
            yl = shape[1]
        if (yh < 0):
            yh = 0
        if (yh > shape[1]):
            yh = shape[1]
        return (xl, xh, yl, yh)

    def __generateContrastAndKurtosis(self, src_img):
        glvlwthfreq = u.getArrayOfGrayLevelsWithFreq(src_img)
        m = np.mean(src_img, axis=None, dtype=float)
        variance = self.__generateVariance(glvlwthfreq, m)
        kurtosis = 0.0
        for tup in glvlwthfreq:
            kurtosis = kurtosis + (np.float_power((float(tup[0]) - m), 4) * (float(tup[1]) / float(src_img.size)))
        kurtosis = kurtosis / np.float_power(variance, 2)
        contrast = float(np.sqrt(variance)) / np.float_power(kurtosis, 0.25)
        return (contrast, kurtosis)

    def __generateVariance(self, matlvls, m):
        gls = matlvls['glvl'].view(dtype=np.uint8)
        frq = matlvls['freq'].view(dtype=np.uint32)
        totpix = frq.sum(axis=None, dtype=float)
        variance = 0.0
        for g in range(0, matlvls.size, 1):
            variance = variance + (np.float_power((float(gls[g]) - m), 2) * (float(frq[g]) / totpix))
        return variance

    def __generateLineLikeness(self, delg_img, theta_img, d=4):
        dirlevels = u.getArrayOfGrayLevelsWithFreq(theta_img, lvldtype=float)
        ditfctcm = np.zeros((dirlevels.size, dirlevels.size), dtype=np.uint32, order='C')
        for i in range(0, (theta_img.shape)[0], 1):
            for j in range(0, (theta_img.shape)[1], 1):
                if (np.fabs(delg_img[i, j]) > 12):
                    x = int(np.round(np.fabs(d * np.cos(theta_img[i, j]))))
                    y = int(np.round(np.fabs(d * np.sin(theta_img[i, j]))))
                    if ((x < 0) | (x >= (theta_img.shape)[0]) | (y < 0) | (y >= (theta_img.shape)[1]) | (np.fabs(delg_img[x, y]) <= 12)):
                        continue
                    else:
                        if ((theta_img[x, y] > (theta_img[i, j] - 0.6)) & (theta_img[x, y] < (theta_img[i, j] + 0.6))):
                            idx1, idx2 = u.search(dirlevels, theta_img[i, j], 0, dirlevels.size-1), u.search(dirlevels, theta_img[x, y], 0, dirlevels.size-1)
                            ditfctcm[idx1, idx2] = ditfctcm[idx1, idx2] + 1
                        else:
                            continue
        return self.__lineLikenessSubPart(ditfctcm, dirlevels)

    def __lineLikenessSubPart(self, ditfctcm, dirlevels):
        dir = 0.0
        for i in range(0, (ditfctcm.shape)[0], 1):
            for j in range(0, (ditfctcm.shape)[0], 1):
                dir = dir + float(ditfctcm[i, j]) * np.cos((((dirlevels[i])[0] - (dirlevels[j])[0]) * 2.0 * np.pi) / dirlevels.size)
        dir = dir / ditfctcm.sum(axis=None, dtype=float)
        return dir

    def getCoarseness(self):
        return self.__coarseness

    def getContrast(self):
        return self.__contrast

    def getKurtosis(self):
        return self.__kurtosis

    def getPrewittHorizontalEdgeImg(self):
        return self.img_hor_x

    def getPrewittVerticalEdgeImg(self):
        return self.img_vert_y

    def getCombinedPrewittImg(self):
        return (self.delg_img).astype(np.uint8)

    def getPrewittDirFactOfImg(self):
        return self.theta_img

    def getLineLikeness(self):
        return self.linelikeness