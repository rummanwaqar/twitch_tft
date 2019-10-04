import cv2
from damage_window import DamageWindowBuilder
from template_matching import CharMatching, LevelMatching
from text_detection import NumberDetector


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

    def setDmg(self, val):
        self.dmg = val

    def __str__(self):
        return "{}[lvl:{}; dmg:{}]".format(self.name, self.level, self.dmg)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if self.name == other.name and self.level == other.level and self.dmg == other.dmg:
            return True
        return False


class Stage(object):
    def __init__(self, index):
        self.open = True
        self.stage = index
        self.champions = []
        self.prev_champion_lists = []

    def isOpen(self):
        return self.open

    def getChampions(self):
        if not self.open and self.champions:
            return self.champions

    def setChampions(self, champions):
        '''
        sets the champions. need same champions for three frames to close the round
        returns True when round closed
        '''
        # we need three iterations with the same champions to close the stage
        self.prev_champion_lists.append(champions)
        # check if lists are the same
        if len(self.prev_champion_lists) == 3:
            if self.prev_champion_lists[0] == self.prev_champion_lists[1] and self.prev_champion_lists[1] == self.prev_champion_lists[2]:
                self.champions = self.prev_champion_lists[0]
                self.open = False
                return True
            else:
                self.prev_champion_lists.pop(0)
        return False

    def __str__(self):
        output = 'Stage {} : '.format(self.stage)
        if self.open:
            output += 'open'
        else:
            output += '['
            for champ in self.champions:
                if champ is not None:
                    output += str(champ) + ', '
            output += ']'
        return output


class GameManager(object):
    def __init__(self):
        self.initialized = False
        self.stages = []
        self.damage_window = None
        self.window_open = False

        # set up detectors
        self.detectors = {
            'champion': None,
            'stars': None,
            'damage': None
        }

    def processFrame(self, img):
        if not self.initialized:
            self.__initialize(img)
        
        if self.initialized:
            # if window was closed and then opened create a new stage
            window_open = self.damage_window.isOpen(img)
            if not self.window_open and window_open:
                self.stages.append(Stage(len(self.stages) + 1))
            self.window_open = window_open

            if self.window_open and self.stages[-1].isOpen():
                if self.stages[-1].setChampions(self.__detectChampions(img)):
                    print(self.stages[-1])

    def draw(self, img):
        if not self.initialized:
            cv2.putText(img, 'NOT INITIALIZED', (50,50), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 255), 2)
        elif not self.window_open:
            cv2.putText(img, 'WINDOW CLOSED', (50,50), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 255), 2)
        else:
            self.damage_window.draw(img)
            stage_output = str(self.stages[-1])
            cv2.putText(img, stage_output, (50,50), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 255), 2)

    def __initialize(self, img):
        self.damage_window = DamageWindowBuilder.InitFromFrame(img, wait_expansion=True)
        if self.damage_window is not None:
            champion_dim = (self.damage_window.damage_bars[0].champion.bbox.w, 
                            self.damage_window.damage_bars[0].champion.bbox.h)
            self.detectors['champion'] = CharMatching('data/champion_templates', champion_dim)
            level_dim = (self.damage_window.damage_bars[0].levelStars.bbox.w, 
                        self.damage_window.damage_bars[0].levelStars.bbox.h)
            self.detectors['stars'] = LevelMatching('data/star_templates', level_dim)
            self.detectors['damage'] = NumberDetector()
            self.initialized = True

    def __detectChampions(self, img):
        championPool = []
        for damage_bar in self.damage_window.damage_bars:
            champion = None
            champion_name = self.detectors['champion'].find_match(damage_bar.champion.getImage(img))
            if champion_name is not None and champion_name != 'none':
                champion = Champion(champion_name)
                level = self.detectors['stars'].find_match(damage_bar.levelStars.getImage(img))
                champion.setLevelFromText(level)
                dmg = self.detectors['damage'].find_match(damage_bar.dmgValue.getImage(img))
                champion.setDmg(dmg)
                if champion.level == 0:
                    champion = None
            championPool.append(champion)
        return championPool