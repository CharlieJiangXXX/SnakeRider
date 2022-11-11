from PGLib.PGGame import *
import pygame
import numpy as np
import matplotlib.pyplot as plt

class SRGameScene(PGScene):
    def __init__(self, game: PGGame):
        bg = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        bg.fill((50, 50, 100))
        wb = Whiteboard(self, 10, 10, 50, 50)
        super().__init__(game, bg)


class Whiteboard(PGObject):
    def __init__(self, parent, x, y, w, h):
        bg = pygame.Surface((500, 500))
        pygame.draw.rect(bg, "white", pygame.Rect(x, y, w, h))
        super().__init__(parent, x, y, bg)
        self.w, self.h = w, h
        self._anal_ = __Whiteboard__(w, h, 8)



class __Whiteboard__:
    def __init__(self, w, h, degree):
        """
        :param h: Height
        :param w: Width
        :param degree: Degree for regression analysis
        """
        self.h, self.w  = h, w
        self.values_x   = [] # x values
        self.values_y   = [] # y values
        self.deg        = degree
        self.p, self.pd = None, None # polynomial expressions of regression and derivative
        self.reg        = None # regression function
        self.regd       = None # derivative/integral regression function

    def add_point(self, x, y):
        """
        :param x: X cord
        :param y: Y cord
        """
        self.values_x.append(x)
        self.values_y.append(y)

    def calc_reg(self, style='dev'):
        """
        :param style: Integrate or derive
        """
        self.p = np.polyfit(self.values_x, self.values_y, self.deg)
        arr = []
        assert style == 'dev' or style == 'int'
        # calculate using power rule on polynomial coeffs
        if style == 'dev':
            for i in range(self.deg):
                arr.append(self.p[i]*(self.deg-i))
        elif style == 'int':
            for i in range(self.deg+1):
                arr.append(self.p[i]/(self.deg-i+1))
            arr.append(0)

        self.pd   = np.array(arr)
        self.reg  = np.poly1d(self.p)
        self.regd = np.poly1d(self.pd)

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
        plt.savefig('Graphs/plt_1.png', bbox_inches='tight', dpi=150)
        plt.clf()
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        plt.plot(ran, self.regd(ran))
        plt.savefig('Graphs/plt_2.png', bbox_inches='tight', dpi=150)
        plt.clf()

    def test(self, X, Y):
        """
        Test functionality on some dataset X and Y.
        """
        self.values_x = X
        self.values_y = Y
        self.calc_reg()
        print(self.p)
        print(self.pd)
        self.show()


# x_test = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,18,19,21,22]
# y_test = [100,90,80,60,60,55,60,65,70,70,75,76,78,79,90,99,99,100]
# WB = Whiteboard(100, 200, 5)
# WB.test(x_test, y_test)
