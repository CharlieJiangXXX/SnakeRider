from PGLib.PGGame import *
from SRGameScene import SRGameScene
from SRHelpScene import SRHelpScene
from SRShopScene import SRShopScene
import sys
from SRLevelSelectionScene import *


class SRMainScene(PGScene):
    def __init__(self, game: PGGame):
        bg = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        bg.fill((50, 50, 100))
        super().__init__(game, bg)
        w, h = game.screen.get_size()

        self._button1 = PGTextButton(self, w/2, 100, "start")
        self._button2 = PGTextButton(self, w/2, 200, "quit")
        self._button3 = PGTextButton(self, w/2, 300, "sound")
        self._button4 = PGTextButton(self, w/2, 400, "help")
        self._button5 = PGTextButton(self, w/2, 500, "shop")
        self._button1.connect_click(self.func1)
        self._button2.connect_click(self.func2)
        self._button3.connect_click(self.func3)
        self._button4.connect_click(self.func4)
        self._button5.connect_click(self.func5)

    def func1(self):
        self._button1.alpha = 150
        SRLevelSelectionScene(self.game).activate()

    def func2(self):
        pygame.quit()
        sys.exit()

    def func3(self):
        self._button3.fade(150)

    def func4(self):
        self._button1.fade(150)
        SRHelpScene(self.game).activate()

    def func5(self):
        self._button5.fade(150)
        SRShopScene(self.game).activate()


game = PGGame()
SRMainScene(game).activate(trans_in="fade")
game.start()
