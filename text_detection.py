import cv2
import os
import re
import pytesseract

class NumberDetector:
    def find_match(self, img):
        # flip image 
        inverted = cv2.bitwise_not(img)
        # convert to text
        text_conversion = pytesseract.image_to_string(inverted)
        # only keep numbers
        output = re.sub("[^0-9]", "", text_conversion)
        return output

import time
if __name__ == '__main__':
    from damage_window import DamageWindowBuilder
    img = cv2.imread('data/league_2.bmp')

    damageWindow = DamageWindowBuilder.InitFromFrame(img)
    detector = NumberDetector()

    for i, bars in enumerate(damageWindow.damage_bars):
        dmgImg = bars.dmgValue.getImage(img)
        start = time.time()
        output = detector.find_match(dmgImg)
        print('took {}'.format(time.time() - start))
        if output:
            print(output)

    cv2.imshow('output', img)
    cv2.waitKey(0)