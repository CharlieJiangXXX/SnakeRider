from PGLib.PGGame import *
from SRHelpScene import SRHelpScene
from SRLevelSelectionScene import SRLevelSelectionScene
from SRShopScene import SRShopScene
from SRGameScene import SRGameScene
import sys
import numpy as np
from pathlib import Path


class SRGame(PGGame):
    def __init__(self, fps: int = 60):
        super().__init__(fps)

        pygame.display.set_caption("Ride With Physics")

        font_path = '../Assets/BH.ttf'
        self.font = pygame.font.Font(font_path, 52)
        self.font_l = pygame.font.Font(font_path, 74)
        self.font_s = pygame.font.Font(font_path, 38)
        self.font_ss = pygame.font.Font(font_path, 20)

        file = Path('high_score.npy')
        file.touch(exist_ok=True)
        try:
            high_score = np.load('high_score.npy')[0]
        except ValueError:
            high_score = 0

    def get_icon(self, name: str):
        return pygame.image.load('../Assets/Icons/' + name + '.png')


class SRImageButton(PGObject):
    def __init__(self, parent, x: float, y: float, sz: int, name: str):
        img = parent.game.get_icon(name)
        img = pygame.transform.scale(img, (sz, sz))
        super().__init__(parent, 0, 0, img)
        self.set_pos_prop(x, y)
        self.connect_hover(True, self.lighten)
        self.connect_hover(False, self.darken)

    def lighten(self):
        self.alpha = 150

    def darken(self):
        self.alpha = 255


class SRMainScene(PGScene):
    def __init__(self, game: SRGame):
        bg = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        w, h = game.screen.get_size()
        im = pygame.image.load('../Assets/notebook.jpg')
        bg.blit(im, (-20, -20))
        super().__init__(game, bg)

        car = game.get_icon("menu_car")
        car = pygame.transform.scale(car, (732, 420))
        car_cropped = pygame.Surface((432, 370))
        car_cropped.blit(car, (-300, 0))
        self._car = PGObject(self, 0, 95, car_cropped)

        title_str = "Ride With Physics"
        title_text = game.font_l.render(title_str, False, "black")
        title = pygame.Surface((600, 200))
        title.blit(title_text, (0, 0))
        self._title = PGObject(self, 0, 0, title)
        self._title.set_pos_prop(1 / 2, 1 / 12)

        self._button1 = SRImageButton(self, 4 / 5, 1 / 2, 150, 'play')
        self._button2 = SRImageButton(self, 60 / 100, 6 / 7, 70, 'quit')
        self._button3 = SRImageButton(self, 72 / 100, 6 / 7, 70, 'sound')
        self._button4 = SRImageButton(self, 84 / 100, 6 / 7, 70, 'help')
        self._button5 = SRImageButton(self, 96 / 100, 6 / 7, 70, 'shop')
        #self._dbg = PGTextButton(self, 0, 0, "debug")
        #self._dbg.connect_click(self.debug)

        self._button1.connect_click(self.start)
        self._button2.connect_click(self.quit)
        self._button3.connect_click(self.sound)
        self._button4.connect_click(self.go_help)
        self._button5.connect_click(self.go_shop)

    def debug(self):
        SRGameScene(self.game).activate()

    def start(self):
        SRLevelSelectionScene(self.game).activate()

    def quit(self):
        pygame.quit()
        sys.exit()

    def sound(self):
        pass

    def go_help(self):
        SRHelpScene(self.game).activate()

    def go_shop(self):
        SRShopScene(self.game).activate()


game = SRGame()
SRMainScene(game).activate(trans_in="fade")
game.start()
