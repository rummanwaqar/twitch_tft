import cv2
from damage_window import DamageWindowBuilder
from template_matching import CharMatching, LevelMatching


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


class GameManager(object):
    def __init__(self):
        self.initialized = False
        self.stage = 1
        self.damage_window = None

        # set up detectors
        self.detectors = {
            'champion': None,
            'stars': None
        }

        # window width (used to make sure the window is full)
        self.window_width = (0, 0)

    def processFrame(self, img):
        if not self.initialized:
            self.damage_window = DamageWindowBuilder.InitFromFrame(img)

            if self.damage_window is not None:
                width = self.damage_window.damage_bars[0].bbox.w
                if self.window_width == width:
                    champion_dim = (self.damage_window.damage_bars[0].champion.bbox.w, 
                                    self.damage_window.damage_bars[0].champion.bbox.h)
                    self.detectors['champion'] = CharMatching('data/champion_templates', champion_dim)
                    level_dim = (self.damage_window.damage_bars[0].levelStars.bbox.w, 
                                self.damage_window.damage_bars[0].levelStars.bbox.h)
                    self.detectors['stars'] = LevelMatching('data/star_templates', level_dim)
                    self.initialized = True
                self.window_width = width

        if self.initialized:
            championPool = []
            for damage_bar in self.damage_window.damage_bars:
                champion = None
                champion_name = self.detectors['champion'].find_match(damage_bar.champion.getImage(img))
                if champion_name is not None and champion_name != 'none':
                    champion = Champion(champion_name)
                    level = self.detectors['stars'].find_match(damage_bar.levelStars.getImage(img))
                    champion.setLevelFromText(level)
                    if champion.level == 0:
                        champion = None
                championPool.append(champion)
            return championPool

    def draw(self, img, champions = None, top_left = (1600, 350), padding = 45):
        if not self.initialized:
            cv2.putText(img, 'NOT INITIALIZED', (50,50), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 255), 2)
        else:
            self.damage_window.draw(img)
            if champions is not None:
                current_pos = top_left
                for champion in champions:
                    cv2.putText(img, str(champion), current_pos, cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 100, 255), 2)
                    current_pos = (current_pos[0], current_pos[1] + padding)
