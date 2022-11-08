from PGLib.PGGame import *

def color_surface(surface, red, green, blue):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:, :, 0] = red
    arr[:, :, 1] = green
    arr[:, :, 2] = blue

class SRLevelButton(PGObject):
    def __init__(self, parent: Type[PGScene], x: int = 0, y: int = 0, level: int = 1):
        star_filled = pygame.image.load('../Assets/star.png').convert_alpha()
        star_empty = star_filled.copy()
        color_surface(star_empty, 120, 78, 240)
        self._obj = PGObject(self, 100, 100, star_empty)
        super().__init__(parent, x, y, img)


class SRLevelSelectionScene(PGScene):
    def __init__(self, game: PGGame):
        bg = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        bg.fill((50, 50, 100))
        super().__init__(game, bg)
