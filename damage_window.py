import cv2
import numpy as np

class Rectangle(object):
    def __init__(self, x, y, w, h):
        '''
        x, y represents top left point
        '''
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def corners(self):
        '''
        returns top-left and bottom-right corners
        '''
        return [(self.x, self.y), (self.x + self.w, self.y + self.h)]

    def offset(self, val):
        self.x += val[0]
        self.y += val[1]

    def draw(self, img, color=(0,0,255), width=1):
        cv2.rectangle(img, self.corners()[0], self.corners()[1], color, width)

    def __repr__(self):
        return '[({},{}),({},{})]'.format(self.x, self.y, self.w, self.h)


class BoundingBoxObject(object):
    def __init__(self, x, y, w, h, color=(0,0,255)):
        cvtInt = lambda x : int(round(x))
        self.bbox = Rectangle(cvtInt(x), cvtInt(y), cvtInt(w), cvtInt(h))
        self.color = color

    def draw(self, img):
        self.bbox.draw(img, self.color)

    def getImage(self, img):
        corners = self.bbox.corners()
        return img[corners[0][1]:corners[1][1],corners[0][0]:corners[1][0]]


class DamageBar(BoundingBoxObject):
    def __init__(self, x, y, w, h):
        super(DamageBar, self).__init__(x, y, w, h, (255,0,0))

        self.champion = BoundingBoxObject(
            self.bbox.x + 2,
            self.bbox.y,
            self.bbox.h,
            self.bbox.h,
            color=(255,0,255)
        )

        self.dmgValue = BoundingBoxObject(
            self.champion.bbox.x + self.champion.bbox.h,
            self.bbox.y,
            self.bbox.w - self.champion.bbox.w,
            self.bbox.h / 2,
            color=(0,0,255)
        )

        self.levelStars = BoundingBoxObject(
            self.champion.bbox.x,
            self.champion.bbox.y + 0.75 * self.champion.bbox.h,
            self.champion.bbox.w,
            self.champion.bbox.h * 0.25,
            color=(0,255,255)
        )

    def draw(self, img):
        super(DamageBar, self).draw(img)
        self.champion.draw(img)
        self.dmgValue.draw(img)
        self.levelStars.draw(img)


class DamageWindow(object):
    def __init__(self, anchor, dim, padding, img=None):
        self.damage_bars = DamageWindow.GenerateDamageBars(anchor, dim, padding, 10)

        # this section is used to test if window is open
        test_dim = (0.07 * dim[0], (dim[1] + padding) * 3 - padding)
        self.open_test_section = BoundingBoxObject(anchor[0] - test_dim[0] - 2, anchor[1], test_dim[0], test_dim[1], (255,255,0))
        self.open_color = np.array([31, 32, 21])
        # if image is provided calculate open region color
        if img is not None:
            self.open_color = np.array(self.GetAverageColor(self.open_test_section.getImage(img)))

    def isOpen(self, img):
        '''
        check if damage window is open
        returns true if open
        '''
        color = np.array(self.GetAverageColor(self.open_test_section.getImage(img)))
        in_range = np.logical_and(color >= self.open_color - 1.5, color <= self.open_color + 1.5)
        return np.all(in_range)

    def draw(self, img):
        for bar in self.damage_bars:
            bar.draw(img)
        self.open_test_section.draw(img)

    @staticmethod
    def GetAverageColor(img):
        return img.mean(axis=0).mean(axis=0)

    @staticmethod
    def GenerateDamageBars(anchor, dim, padding, n_bars):
        x, y = anchor
        bars = []
        for i in range(n_bars):
            bars.append(DamageBar(x, y, dim[0], dim[1]))
            y += (padding + dim[1])
        return bars


class DamageWindowBuilder(object):
    NUM_BARS = 10
    
    # window width (used to make sure the window is fully expanded)
    WINDOW_WIDTH = 0

    @staticmethod
    def InitFromCoods(top_left = [1777, 326], width = 128, height = 36, padding = 9):
        return DamageWindow(top_left, (width, height), padding)

    @staticmethod
    def InitFromFrame(img, wait_expansion = False):
        '''
        @param wait_expansion: if true we wait for the window to fully expand
        returns None if cannot be initialized
        '''
        # get ROI with damage bar
        (x_offset, y_offset), roi = DamageWindowBuilder.GetRoi(img, [0.88, 1], [0.13, 0.78])

        # get empty rectangles in damage bar
        rects = DamageWindowBuilder.GetDamageRects(roi)
        # we need at least 3 rects to succeed
        if len(rects) < 3:
            return
        # correct offsets due to ROI
        for rect in rects:
            rect.offset((x_offset, y_offset))
        
        # get filtered parameters
        top_left, width, height, padding = DamageWindowBuilder.GetAverageRectsParams(rects)

        # interpolate rects above if needed
        n_rects_above = DamageWindowBuilder.NUM_BARS - len(rects)
        if n_rects_above > 0:
            top_left[1] = top_left[1] - (height + padding) * n_rects_above

        if not wait_expansion or DamageWindowBuilder.WINDOW_WIDTH == width:
            return DamageWindow(top_left, (width, height), padding, img)
        else:
            DamageWindowBuilder.WINDOW_WIDTH = width
            return

    @staticmethod
    def GetDamageRects(img):
        '''
        get rectangles from empty boxes in damage bar
        '''
        # color threshold limits
        COLOR_THRESHOLD = [(24, 22, 13), (28, 25, 16)]
        # minimum rectangle area
        MIN_AREA = 1000

        # get binary image
        bin_img = cv2.inRange(img, COLOR_THRESHOLD[0], COLOR_THRESHOLD[1])
        # open the image to remove noise
        bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

        # find contours
        _, contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_NONE)

        # get rectangles from contours
        rects = []
        for contour in contours:
            # filter contours by area
            if cv2.contourArea(contour) > MIN_AREA:
                rects.append(Rectangle(*cv2.boundingRect(contour)))
        return rects

    @staticmethod
    def GetAverageRectsParams(rects):
        '''
        calculate averaged values for top_left, (width, height), padding
        '''
        # helper for averages
        avg = lambda x : int(round(sum(x)/float(len(x))))
        
        # get average width, height and top_x
        width = avg([r.w for r in rects])
        height = avg([r.h for r in rects])
        top_x = avg([r.x for r in rects])

        top_ys = sorted([r.y for r in rects])
        n_rects = len(rects)

        # calculate average padding in y
        padding = avg([top_ys[i+1] - top_ys[i] - height for i in range(n_rects - 1)])

        # get best top_y point by extrapolating each point as top point and averaging
        top_y = avg([top_ys[i] - (height + padding) * i for i in range(n_rects)])

        return [top_x, top_y], width, height, padding
    
    @staticmethod
    def GetRoi(img, x_ratio = [0,1], y_ratio=[0,1]):
        '''
        get image roi from ratios
        return (top_left), roi_img
        '''
        height, width, _ = img.shape
        x_limits = np.rint(np.array(x_ratio) * width).astype(int)
        y_limits = np.rint(np.array(y_ratio) * height).astype(int)

        return (x_limits[0], y_limits[0]), img[y_limits[0]:y_limits[1], x_limits[0]:x_limits[1]]


if __name__ == '__main__':
    img = cv2.imread('data/start.bmp')
    # img = cv2.imread('data/league_1.bmp')

    damageWindow = DamageWindowBuilder.InitFromFrame(img)
    damageWindow.draw(img)

    cv2.imshow('final', img)
    cv2.waitKey(0)