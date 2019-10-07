import cv2
import os

class TemplateMatching():
    def __init__(self, template_loc, dim):
        self.dim = dim
        self.templates = self.load(template_loc)
        print("Loaded {} templates".format(len(self.templates)))

    def load(self, folder):
        templates = {}
        files = [f for f in os.listdir(folder) if f.endswith(".png")]
        for f in files:
            template = cv2.imread(os.path.join(folder, f), 0)
            template = cv2.resize(template, self.dim)
            templates[f.split('.')[0]] = template
        return templates

    def preprocess(self, img):
        return img

    def find_match(self, img):
        img = self.preprocess(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        maximum = 0
        match = None
        for template_name, template in self.templates.items():
            res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            res = res.flatten()[0]
            if res > maximum:
                maximum = res
                match = template_name
        return match


class CharMatching(TemplateMatching):
    def __init__(self, template_loc, dim):
        TemplateMatching.__init__(self, template_loc, dim)
        for _, template in self.templates.items():
            template = self.preprocess(template)
        
    def preprocess(self, img):
        # remove the last 20% of each image to remove stars at the bottom
        bottomLimit = int(round(self.dim[1] * 0.8))
        return img[:bottomLimit, :]


class LevelMatching(TemplateMatching):
    def __init__(self, template_loc, dim):
        TemplateMatching.__init__(self, template_loc, dim)
