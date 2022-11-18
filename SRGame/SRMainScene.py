from PGLib.PGGame import *
from SRHelpScene import SRHelpScene
from SRLevelSelectionScene import SRLevelSelectionScene
from SRShopScene import SRShopScene
import sys


class img_button(PGObject):
    def __init__(self, parent, x, y, sz, img_src):
        img = pygame.image.load(img_src)
        img = pygame.transform.scale(img, (sz, sz))
        super().__init__(parent, x, y, img)


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

        self._button1 = img_button(self, w/2-50, 200, 100, '../Assets/start.png')
        self._button2 = img_button(self, w/2, h-100, 50, '../Assets/quit.png')
        self._button3 = img_button(self, w/2+100, h-100, 50, '../Assets/sound.png')
        self._button4 = img_button(self, w/2+200, h-100, 50, '../Assets/help.png')
        self._button5 = img_button(self, w/2+300, h-100, 50, '../Assets/shop.png')
        self._button1.connect_click(self.start)
        self._button2.connect_click(self.quit)
        self._button3.connect_click(self.sound)
        self._button4.connect_click(self.go_help)
        self._button5.connect_click(self.go_shop)



    def start(self):
        self._button1.fade(150)
        SRLevelSelectionScene(self.game).activate()

    def quit(self):
        pygame.quit()
        sys.exit()

    def sound(self):
        self._button3.fade(150)

    def go_help(self):
        self._button4.fade(150)
        SRHelpScene(self.game).activate()

    def go_shop(self):
        self._button5.fade(150)
        SRShopScene(self.game).activate()


game = PGGame()
SRMainScene(game).activate(trans_in="fade")
game.start()
