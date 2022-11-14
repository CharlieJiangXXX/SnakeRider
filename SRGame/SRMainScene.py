from PGLib.PGGame import *
from SRHelpScene import SRHelpScene
from SRLevelSelectionScene import SRLevelSelectionScene
from SRShopScene import SRShopScene
import sys

class img_button(PGObject):
    def __init__(self, parent, x, y, img_src):
        img = pygame.image.load(img_src)
        img = pygame.transform.scale(img, (100, 100))
        super().__init__(parent, x, y, img)

class SRMainScene(PGScene):
    def __init__(self, game: PGGame):
        bg = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        bg.fill((50, 50, 100))
        super().__init__(game, bg)
        w, h = game.screen.get_size()
        self._button1 = img_button(self, w/2-50, 200, '../Assets/start.png')
        self._button2 = img_button(self, w/2+25, 300, '../Assets/quit.png')
        self._button3 = img_button(self, w/2+125, 300, '../Assets/sound.png')
        self._button4 = img_button(self, w/2+225, 300, '../Assets/help.png')
        self._button5 = img_button(self, w/2+325, 300, '../Assets/shop.png')
        self._button1.connect_click(self.start)
        self._button2.connect_click(self.quit)
        self._button3.connect_click(self.sound)
        self._button4.connect_click(self.func4)
        self._button5.connect_click(self.func5)



    def start(self):
        self._button1.fade(150)
        SRLevelSelectionScene(self.game).activate()

    def quit(self):
        pygame.quit()
        sys.exit()

    def sound(self):
        self._button3.fade(150)

    def func4(self):
        self._button4.fade(150)
        SRHelpScene(self.game).activate()

    def func5(self):
        self._button5.fade(150)
        SRShopScene(self.game).activate()


game = PGGame()
SRMainScene(game).activate(trans_in="fade")
game.start()
