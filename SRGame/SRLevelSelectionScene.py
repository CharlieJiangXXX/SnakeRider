from PGLib.PGGame import *


class SRLevelSelectionScene(PGScene):
    def __init__(self, game: PGGame):
        bg = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        bg.fill((50, 50, 100))
        super().__init__(game, bg)
