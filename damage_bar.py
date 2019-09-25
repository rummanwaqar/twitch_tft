import cv2

class Point2D(object):
    """
    simple 2d point
    """
    def __init__(self, x, y):
        self.data = (x, y)

    def __getitem__(self, key):
        if key == 0 or key == 'x':
            return self.data[0]
        elif key == 1 or key == 'y':
            return self.data[1]
        else:
            return None

    def __add__(self, other):
        if isinstance(other, (int, long)):
            return Point2D(self.data[0] + other, self.data[1] + other)
        else:
            return Point2D(self.data[0] + other.data[0], self.data[1] + other.data[1])

class DamageBar(object):
    """
    The damage bar is currently built with hardcoded values.
    The bottom left point on the last bar is used as an anchor point.
    Everything is calculated from this point
    """
    ANCHOR = Point2D(1777, 767)
    BAR_DIM = Point2D(128, 36)
    BAR_PADDING = Point2D(0, 9)
    NUM_BARS = 10

    # character relative to bar
    CHAR_DIM = Point2D(36, 36)
    CHAR_REL_OFFSET = Point2D(3, 0)

    # level (stars) relative to character
    LEVEL_DIM = Point2D(36, 10)
    LEVEL_REL_OFFSET = Point2D(0, 30)

    def __init__(self, index):
        # calc abs coods of damage bar on screen for index
        self.bar_topleft = Point2D(self.ANCHOR[0], 
            self.ANCHOR[1] - ((self.NUM_BARS - 1 - index) * 
            (self.BAR_DIM[1] + self.BAR_PADDING[1])) - self.BAR_DIM[1])
        
        # calc abs character coods
        self.char_topleft = self.bar_topleft + self.CHAR_REL_OFFSET

        # calc abs level coods
        self.level_topleft = self.char_topleft + self.LEVEL_REL_OFFSET

    def __get_item(self, topleft, dim, img=None):
        # return coods if no image, otherwise return image ROI
        point1 = topleft.data
        point2 = (topleft + dim).data
        if img is None:
            return (point1, point2)
        else:
            return img[point1[1]:point2[1], point1[0]:point2[0]]

    def get_bar(self, img=None):
        return self.__get_item(self.bar_topleft, self.BAR_DIM, img)
    
    def get_char(self, img=None):
        return self.__get_item(self.char_topleft, self.CHAR_DIM, img)

    def get_level(self, img=None):
        return self.__get_item(self.level_topleft, self.LEVEL_DIM, img)

    def draw(self, img):
        """ draws bar, char and level on image """
        bar_coods = self.get_bar()
        char_coods = self.get_char()
        level_coods = self.get_level()
        cv2.rectangle(img, bar_coods[0], bar_coods[1], (255, 0, 0), 1)
        cv2.rectangle(img, char_coods[0], char_coods[1], (0, 0, 255), 1)
        cv2.rectangle(img, level_coods[0], level_coods[1], (0, 255, 0), 1)

if __name__ == '__main__':
    img = cv2.imread('data/league_1.bmp')
    for i in range(10):
        bar = DamageBar(i)
        bar.draw(img)
    cv2.imshow('Window', img)
    cv2.waitKey(0)