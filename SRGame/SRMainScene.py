from PGLib.PGGame import *


class SRMainScene(PGScene):
    def __init__(self, game: PGGame):
        bg = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        bg.fill((50, 50, 100))
        super().__init__(game, bg)
        self._button1 = PGTextButton(self, 0, 0, "googoo")
        self._button1.connect_click(self.func1)

    def func1(self):
        self._button1.fade(150)
        self._button1.fade(255)


game = PGGame()
SRMainScene(game).activate(trans_in="fade")
game.start()
