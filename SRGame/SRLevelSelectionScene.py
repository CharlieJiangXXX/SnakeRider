from PGLib.PGGame import *


def color_surface(surface, red, green, blue):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:, :, 0] = red
    arr[:, :, 1] = green
    arr[:, :, 2] = blue

_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, gfcolor=pygame.Color('dodgerblue'), ocolor=(255, 255, 255), opx=2):
    font = pygame.font.SysFont(None, 64)
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf


class SRLevelButton(PGFrame):
    def __init__(self, parent, x: int = 0, y: int = 0, level: int = 1):
        radius = 40
        super().__init__(parent, (radius * 2, 105), x, y)
        circle = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(circle, "blue", (radius, radius), radius)
        self._circle = PGObject(self, 0, 0, circle)

        star_filled = pygame.image.load('../Assets/Icons/star.png').convert_alpha()
        star_empty = star_filled.copy()
        color_surface(star_empty, 120, 78, 240)
        star_empty = pygame.transform.smoothscale(star_empty, (20, 20))
        for i in range(3):
            obj = PGObject(self, 0, 0, star_empty)
            obj.pos = (5 + i * 25, 85)

        number = render(str(level))
        number_obj = PGObject(self, 25, 20, number)
        number_obj.set_pos_prop(1 / 2, 3 / 8)


class SRLevelSelectionScene(PGScene):
    def __init__(self, game: PGGame):
        bg = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        bg.fill((50, 50, 100))
        super().__init__(game, bg)
        self._buttons = []

        for i in range(15):
            x = 10 + i * 120
            y = 0
            while x > self._screen.get_width():
                x -= self._screen.get_width()
                y += 130
            self._buttons.append(SRLevelButton(self, x, y, i + 1))

        self._buttons[0].connect_click(self.hi)

    def hi(self):
        print("hi")