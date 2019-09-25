import cv2
import sys
from damage_bar import DamageBar
from template_matching import CharMatching, LevelMatching

charMatcher = CharMatching('data/champion_templates')
levelMatcher = LevelMatching('data/star_templates')

class Champion(object):
    """
    represent a champion
    """
    def __init__(self, name, level=1, dmg=0):
        self.name = name
        self.level = level
        self.dmg = dmg

    def setLevelFromText(self, text):
        if text == '1star':
            self.level = 1
        elif text == '2stars':
            self.level = 2
        elif text == '3stars':
            self.level = 3
        else:
            # unknown level
            self.level = 0 

    def __str__(self):
        return "{}[lvl:{}]".format(self.name, self.level)

    def __repr__(self):
        return self.__str__()


def draw(img, champions, pos, padding):
    current_pos = pos
    for champion in champions:
        cv2.putText(img, str(champion), current_pos, cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 100, 255), 2)
        current_pos = (current_pos[0], current_pos[1] + padding)


def process_frame(img, drawing=False):
    championPool = []
    for i in range(DamageBar.NUM_BARS):
        dmg_bar = DamageBar(i)
        champion = None
        champion_name = charMatcher.find_match(dmg_bar.get_char(img))
        if champion_name:
            champion = Champion(champion_name)
            level = levelMatcher.find_match(dmg_bar.get_level(img))
            champion.setLevelFromText(level)
        championPool.append(champion)

    if drawing:
        draw(img, championPool, (1600, 350), 45)
    return championPool


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python main.py img|video')
        exit(1)
    
    # process video
    if sys.argv[1].endswith('.mp4'):
        video = cv2.VideoCapture(sys.argv[1])
        while True:
            ret, frame = video.read()
            if not ret:
                break
            process_frame(frame, True)
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            cv2.imshow('Video', frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        video.release()
    # process image
    elif sys.argv[1].endswith('.jpg') or sys.argv[1].endswith('.bmp'):
        img = cv2.imread(sys.argv[1])
        champions = process_frame(img, True)
        cv2.imshow('Result', img)
        cv2.waitKey(0)

    cv2.destroyAllWindows()
    