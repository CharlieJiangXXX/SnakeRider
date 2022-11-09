from PGLib.PGGame import *
import numpy as np
import matplotlib.pyplot as plt

class SRGameScene(PGScene):
    def __init__(self, game: PGGame):
        bg = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        bg.fill((50, 50, 100))
        super().__init__(game, bg)


class Whiteboard:
    def __init__(self, h, w, degree):
        """
        :param h: Height
        :param w: Width
        :param degree: Degree for regression analysis
        """
        self.h, self.w  = h, w
        self.values_x   = [] # x values
        self.values_y   = [] # y values
        self.deg        = degree
        self.p, self.pd = None, None # polynomial expressions of regression and derevaative
        self.reg        = None # regression function
        self.regd       = None # derevative/integral regression function

    def add_point(self, x, y):
        """
        :param x: X cord
        :param y: Y cord
        """
        self.values_x.append(x)
        self.values_y.append(y)

    def calc_reg(self, style='int'):
        """
        :param style: Integrate or derive
        """
        self.p = np.polyfit(self.values_x, self.values_y, self.deg)
        arr = []
        assert style == 'dev' or style == 'int'
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

    def show(self):
        """
        Plot output
        """
        ran = np.linspace(min(self.values_x), max(self.values_x), 300)
        plt.plot(ran, self.reg(ran))
        plt.plot(ran, self.regd(ran))
        plt.show()

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
# WB = whiteboard(100, 200, 5)
# WB.test(x_test, y_test)
