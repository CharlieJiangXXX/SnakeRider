import pygame, sys
import numpy as np
from os import chdir
from matplotlib import pyplot as plt

# global variables
screen_width = 720
screen_height = 480

# chdir('SnakeRider')
box   = pygame.image.load('Assets/frame.png')
back  = pygame.image.load('Assets/notebook.jpg')
play  = pygame.image.load('Assets/play.png')
erase = pygame.image.load('Assets/erase.png')

'''---------------------------------SPRITES/CLASSES---------------------'''


class Whiteboard(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, degree, sprite):
        super(Whiteboard, self).__init__()
        self.h, self.w  = h, w
        self.x, self.y  = x, y # x, y cords
        self.values_x   = [] # x values
        self.values_y   = [] # y values
        self.deg        = degree
        self.p, self.pd = None, None # polynomial expressions of regression and derivative
        self.reg        = None # regression function
        self.regd       = None # derivative/integral regression function
        self.sprite     = pygame.transform.scale(sprite, (w, h))

    def add_point(self, x, y):
        """
        :param x: X cord
        :param y: Y cord
        """
        self.values_x.append(x)
        self.values_y.append(y)

    def calc_reg(self, style='none'):
        """
        :param style: Integrate or derive
        """
        self.p = np.polyfit(self.values_x, self.values_y, self.deg)
        self.reg = np.poly1d(self.p)
        arr = []
        assert style == 'dev' or style == 'int' or style == 'none'
        # calculate using power rule on polynomial coeffs

        if style == 'none':
            return None
        elif style == 'dev':
            for i in range(self.deg):
                arr.append(self.p[i]*(self.deg-i))
        elif style == 'int':
            for i in range(self.deg+1):
                arr.append(self.p[i]/(self.deg-i+1))
            arr.append(0)

        self.pd   = np.array(arr)
        self.regd = np.poly1d(self.pd)

    def compute_opt(self):
        x_vals  = np.linspace(25, self.w-25, self.w-50)
        y_vals  = self.reg(x_vals) # calculate regression representation over the range
        y_vals += 20
        x_vals += 20
        return list(np.stack((x_vals, y_vals)).T)

    def save(self):
        """
        saves output
        """
        x_min = min(self.values_x)
        x_max = max(self.values_x)
        y_min = min(self.values_y)
        y_max = max(self.values_y)
        ran = np.linspace(x_min, x_max, 300) # range
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        plt.plot(ran, self.reg(ran))
        plt.savefig('SnakeRider/SRGame/Graphs/plt_1.png', bbox_inches='tight', dpi=150)
        plt.clf()
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        plt.plot(ran, self.regd(ran))
        plt.savefig('SnakeRider/SRGame/Graphs/plt_2.png', bbox_inches='tight', dpi=150)
        plt.clf()

    def clear(self):
        self.values_x = []  # x values
        self.values_y = []  # y values


class Icon(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, sprite):
        super(Icon, self).__init__()
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.sprite    = pygame.transform.scale(sprite, (w, h))
        self.is_light  = False

    def is_on(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.x < mouse_x < self.x + self.w and self.y < mouse_y < self.y + self.h

    def lighten(self):
        if not self.is_light:
            self.sprite.fill((100, 100, 100), special_flags=pygame.BLEND_RGB_SUB)
            self.is_light = True

    def darken(self):
        if self.is_light:
            self.sprite.fill((100, 100, 100), special_flags=pygame.BLEND_RGB_ADD)
            self.is_light = False


def main():
    '''---------------------------------SETUP-------------------------------'''
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Game Title')
    wb1     = Whiteboard(20, 20, 320, 340, 5, box)
    wb2     = Whiteboard(380, 20, 320, 340, 5, box)
    eraser  = Icon(40, 380, 74, 74, erase)
    draw    = Icon(325, 380, 74, 74, play)
    arrived = []
    rolling_y = 0
    hold = False
    smooth = False

    eraser.lighten()
    draw.lighten()

    '''----------------------------------LOOP-------------------------------'''
    while True:
        # Handling events
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                hold = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if eraser.is_on() and not hold:
                    arrived = []
                    wb1.clear()
                    smooth = False
                hold = True

        if hold and not smooth:
            if wb1.x + 25 < mouse_x < wb1.x + wb1.w - 25 and wb1.y + 25 < mouse_y < wb1.y + wb1.h - 25:
                arrived.append((mouse_x, mouse_y))
                wb1.add_point(mouse_x-wb1.x, mouse_y - wb1.y)
                # wb1.add_point(mouse_x-wb1.x, wb1.h//2 - (mouse_y - wb1.y))

        if eraser.is_on():
            eraser.lighten()
        elif eraser.is_light:
            eraser.darken()

        if draw.is_on():
            draw.lighten()
        elif draw.is_light:
            draw.darken()

        if not hold and arrived != [] and not smooth:
            wb1.calc_reg('dev')
            arrived = wb1.compute_opt()

            # remove all out of range values that might come from regression
            l = len(arrived)
            for i in range(l):
                if not wb1.y + 25 < arrived[l - i - 1][1] < wb1.y + wb1.h - 25:
                    arrived.pop(l - i - 1)
            smooth = True

        # Updating Sprites

        # Drawing
        screen.fill('white')
        screen.blit(back, (-20, -20))
        screen.blit(wb1.sprite, (wb1.x, wb1.y))
        screen.blit(wb2.sprite, (wb2.x, wb2.y))
        screen.blit(eraser.sprite, (eraser.x, eraser.y))
        screen.blit(draw.sprite, (draw.x, draw.y))

        if len(arrived) > 1:
            pygame.draw.lines(screen, 'black', False, arrived, 4)

        # Updating the window
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()