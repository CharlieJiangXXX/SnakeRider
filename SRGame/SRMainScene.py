from PGLib.PGGame import *
from SRHelpScene import SRHelpScene
from SRLevelSelectionScene import SRLevelSelectionScene
from SRShopScene import SRShopScene
import sys


class SRImageButton(PGObject):
    def __init__(self, parent, x: float, y: float, sz: int, img_src):
        img = pygame.image.load(img_src)
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
    def __init__(self, game: PGGame):
        bg = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        w, h = game.screen.get_size()
        im = pygame.image.load('../Assets/notebook.jpg')
        bg.blit(im, (-20, -20))
        font = pygame.font.Font('../Assets/BH.ttf', 52)
        title_str = "RIDE WITH PHYSICS"
        title = font.render(title_str, False, "black")
        a, b = font.size(title_str)
        bg.blit(title, (w/2-a/2, 100))
        super().__init__(game, bg)

        self._button1 = SRImageButton(self, 1 / 2, 1 / 2, 100, '../Assets/start.png')
        self._button2 = SRImageButton(self, 1 / 5, 3 / 4, 50, '../Assets/quit.png')
        self._button3 = SRImageButton(self, 2 / 5, 3 / 4, 50, '../Assets/sound.png')
        self._button4 = SRImageButton(self, 3 / 5, 3 / 4, 50, '../Assets/help.png')
        self._button5 = SRImageButton(self, 4 / 5, 3 / 4, 50, '../Assets/shop.png')
        self._button1.connect_click(self.start)
        self._button2.connect_click(self.quit)
        self._button3.connect_click(self.sound)
        self._button4.connect_click(self.go_help)
        self._button5.connect_click(self.go_shop)

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


game = PGGame()
SRMainScene(game).activate(trans_in="fade")
game.start()
