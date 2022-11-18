import os
from random import randint
import pygame, sys
import numpy as np
from os import chdir
from matplotlib import pyplot as plt
from math import atan, degrees

# global variables
screen_width = 720
screen_height = 480


'''---------------------------------SPRITES/CLASSES---------------------'''


def norm(arr, min, max, l_bound, u_bound):
    """
    Normalize array into a certain range
    :param arr: array
    :param min: desired min
    :param max: desired max
    :param l_bound: current lower bound
    :param u_bound: current upward bound
    :return: new array
    """
    assert u_bound > l_bound
    assert max > min
    factor = (max - min)/(u_bound-l_bound)
    dist   = [x-(u_bound+l_bound)/2 for x in arr]
    dist   = [x*factor for x in dist]
    dist   = [x + (max+min)/2 for x in dist]
    return np.array(dist)


class Whiteboard(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, degree, sprite, linesprite):
        """
        :param x: x cord
        :param y: y cord
        :param w: width
        :param h: height
        :param degree: degree of fit for polynomial
        :param sprite: sprite
        :param linesprite:  sprite for horizontal line
        """
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
        self.sprite.blit(pygame.transform.scale(linesprite, (w-50, (w-50)*0.034)), (25, h//2))

    def add_point(self, x, y):
        """
        Adds a point to the log.
        :param x: X cord
        :param y: Y cord
        """
        self.values_x.append(x)
        self.values_y.append(y)

    def calc_reg(self, style='none'):
        """
        Sets the sekf pd regression value to the regressed function, assuming original bounds were between (0,4) for x
        and (-2,2) for y.
        :param style: Integrate, derive, or none.
        """
        self.p = np.polyfit(self.values_x, self.values_y, self.deg)
        self.reg = np.poly1d(self.p)
        arr = []
        assert style == 'dev' or style == 'int' or style == 'none'

        # adjust for center value
        x_adj = norm(self.values_x, 0, 4, 25, self.w-25)
        y_adj = norm(self.values_y, -2, 2, 25, self.h-25)
        y_adj = [-1*y for y in y_adj]
        p_adj = np.polyfit(x_adj, y_adj, self.deg)

        # calculate using power rule on polynomial coeffs
        if style == 'none':
            arr = p_adj
        elif style == 'dev':
            for i in range(self.deg):
                arr.append(p_adj[i]*(self.deg-i))
        elif style == 'int':
            for i in range(self.deg+1):
                arr.append(p_adj[i]/(self.deg-i+1))
            arr.append(0)

        self.pd   = np.array(arr)
        self.regd = np.poly1d(arr)

    def compute_opt(self):
        """
        Calculate regression from the self regression function, stacks into raw coordinate points.
        """
        x_vals  = np.linspace(25, self.w-25, self.w-50)
        y_vals  = self.reg(x_vals) # calculate regression representation over the range
        y_vals += 20
        x_vals += 20
        return list(np.stack((x_vals, y_vals)).T)

    def compute_pd_opt(self, target):
        """
        Computes the regression from the derivative regression function, applying the scaling from y in (-2,
        2) and x in (0,4) to the entire plane.
        :param target: Object to draw onto.
        """
        x_vals  = np.linspace(0, 4, self.w-50)
        y_vals  = self.regd(x_vals) # calculate regression representation over the range
        x_vals  = norm(x_vals, 25, self.w-25, 0.1, 3.9) # leniency bounds
        y_vals  = norm(y_vals, 0, self.h, -2, 2)
        y_vals *= -1
        y_vals += target.h+20
        x_vals += target.x
        return list(np.stack((x_vals, y_vals)).T)

    def save(self):
        """
        Saves output for testing purposes as a plt graph.
        """
        x_min = min(self.values_x)
        x_max = max(self.values_x)
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
        """
        Clears values.
        """
        self.values_x = []  # x values
        self.values_y = []  # y values

    def import_pd(self, regd):
        """
        Setter for regd, used when importing the calculated regression onto the other whiteboard.
        """
        self.regd = regd


class Icon(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, sprite):
        """
        :param x: x cord
        :param y: y cord
        :param w: width
        :param h: height
        :param sprite: sprite
        """
        super(Icon, self).__init__()
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.sprite    = pygame.transform.scale(sprite, (w, h))
        self.is_light  = False # whether being hovered on or not

    def is_on(self):
        """
        Checks if the mouse is on the icon or not.
        :return: True or False
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.x < mouse_x < self.x + self.w and self.y < mouse_y < self.y + self.h

    def lighten(self):
        """
        Lightens sprite color.
        """
        if not self.is_light:
            self.sprite.fill((100, 100, 100), special_flags=pygame.BLEND_RGB_SUB)
            self.is_light = True

    def darken(self):
        """
        Darkens sprite color.
        """
        if self.is_light:
            self.sprite.fill((100, 100, 100), special_flags=pygame.BLEND_RGB_ADD)
            self.is_light = False


class Collideable(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, sprite):
        """
        :param x: x cord
        :param y: y cord
        :param w: width
        :param h: height
        :param sprite: sprite
        """
        super(Collideable, self).__init__()
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.sprite = pygame.transform.scale(sprite, (w, h))

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    @property
    def mask(self):
        return pygame.mask.from_surface(self.sprite)

    def pop(self):
        """
        Disappear object.
        """
        alpha = self.sprite.get_alpha()
        if alpha > 5:
            self.sprite.set_alpha(alpha-5)
        elif alpha != 0:
            self.sprite.set_alpha(0)

    def clear(self):
        """
        Resets object.
        """
        self.sprite.set_alpha(255)


class Car(Collideable):
    def __init__(self, x, y, w, h, sprite):
        super(Car, self).__init__(x-w/2+20, y-h/2, w, h, sprite)
        self.step = 0
        self.sprite_i = self.sprite
        self.x_i, self.y_i = x-w/2+20, y-h/2

    def update(self, arrived_2):
        """
        Drive over the line.
        :param arrived_2: Coordinate points to walk through
        """
        self.x, self.y = arrived_2[self.step]
        slope = arrived_2[self.step + 1][1]-self.y
        ang = degrees(atan(slope)) # calculate angle to drive
        self.sprite = pygame.transform.rotate(self.sprite_i, -ang) # rotate
        self.w, self.h = self.sprite.get_size()
        self.x -= self.w/2  # correct for misalignment
        self.y -= self.h/2
        if self.step < len(arrived_2)-2:
            self.step += 1
            return True
        else:
            return False

    def clear(self):
        """
        Reset.
        """
        self.step = 0
        self.sprite = self.sprite_i
        self.x, self.y = self.x_i, self.y_i

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    @property
    def mask(self):
        return pygame.mask.from_surface(self.sprite)


def game_start():

    '''---------------------------------SETUP-------------------------------'''

    order = {'x': 0, 'v': 1, 'a': 2}
    possibilities = [['a', 'v'], ['v', 'a'], ['x', 'v'], ['v', 'x']]
    left_prop, right_prop = possibilities[randint(0, 3)]
    streak = 0

    # load image assets
    font = pygame.font.Font('Assets/BH.ttf', 52)
    font_s = pygame.font.Font('Assets/BH.ttf', 38)
    font_ss = pygame.font.Font('Assets/BH.ttf', 20)

    high_score = np.load('high_score.npy')[0]

    box = pygame.image.load('Assets/frame.png')
    back = pygame.image.load('Assets/notebook.jpg')
    play = pygame.image.load('Assets/play.png')
    erase = pygame.image.load('Assets/erase.png')
    line = pygame.image.load('Assets/line.png')
    star = pygame.image.load('Assets/star.png')
    flag_i = pygame.image.load('Assets/finishflag.png')
    car_t  = pygame.image.load('Assets/car.png') if high_score < 100 else pygame.image.load('Assets/car_g.png')
    exit_i = pygame.image.load('Assets/exit.png')

    # load sound assets

    click        = pygame.mixer.Sound('Assets/click.wav')
    collect_star = pygame.mixer.Sound('Assets/collect_star.wav')
    collect_flag = pygame.mixer.Sound('Assets/collect_flag.wav')
    car_go       = pygame.mixer.Sound('Assets/car_sound.wav')
    lose         = pygame.mixer.Sound('Assets/cat.wav')

    wb1    = Whiteboard(20, 20, 320, 340, 7, box, line)
    wb2    = Whiteboard(380, 20, 320, 340, 7, box, line)
    eraser = Icon(40, 380, 74, 74, erase)
    go     = Icon(150, 380, 74, 74, play)
    exit   = Icon(610, 370, 94, 94, exit_i)
    arrived = [] # points to plot on LHS
    arrived_2 = [] # points to plot on RHS

    star_1 = Collideable(wb2.x+60,  wb2.y+wb2.h/2-26, 52, 52, star)
    star_2 = Collideable(wb2.x+110,  wb2.y+wb2.h/2-26, 52, 52, star)
    star_3 = Collideable(wb2.x+160,  wb2.y+wb2.h/2-26, 52, 52, star)

    flag = Collideable(wb2.x+210, wb2.y+wb2.h/2-50, 86, 100, flag_i)
    car  = Car(wb2.x, wb2.y + wb2.h/2, 64, 48, car_t)

    hold   = False # is the mouse held down
    smooth = False  # has regression been calculated
    start  = False # has the start button been pressed

    star_1_received = False
    star_2_received = False
    star_3_received = False
    flag_received   = False

    leave = False

    eraser.lighten()
    go.lighten()
    exit.lighten()

    def render(obj):
        """
        Blits an object with its coordinate points.
        :param obj: object to render
        """
        screen.blit(obj.sprite, (obj.x, obj.y))

    '''----------------------------------LOOP-------------------------------'''
    while True:
        # Handling events
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # update labels
        stk_label = font_s.render(f"streak: {streak}", False, 'black')
        hsr_label = font_s.render(f"high score: {high_score}", False, 'black')
        fct_label = font_ss.render("reach 100 to unlock a secret.", False, 'black')
        lhs_label = font.render(left_prop, False, 'black')
        rhs_label = font.render(right_prop, False, 'black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                hold = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                click.play() # play click sound

                if eraser.is_on() and not hold and not start:  # eraser button pressed
                    arrived   = []
                    arrived_2 = []
                    wb1.clear()
                    car.clear()
                    star_1.clear()
                    star_2.clear()
                    star_3.clear()
                    flag.clear()

                    smooth = False
                    start  = False
                    star_1_received = False
                    star_2_received = False
                    star_3_received = False
                    flag_received = False

                elif go.is_on() and not hold and smooth: # go button pressed
                    car_go.play()
                    start = True

                elif exit.is_on() and not hold:
                    leave = True # breaks into return statement

                hold = True

        if hold and not smooth:
            if wb1.x + 25 < mouse_x < wb1.x + wb1.w - 25 and wb1.y + 25 < mouse_y < wb1.y + wb1.h - 25:
                arrived.append((mouse_x, mouse_y))
                wb1.add_point(mouse_x-wb1.x, mouse_y - wb1.y)
                # wb1.add_point(mouse_x-wb1.x, wb1.h//2 - (mouse_y - wb1.y))

        # button highlighting
        if eraser.is_on():
            eraser.lighten()
        elif eraser.is_light:
            eraser.darken()

        if go.is_on():
            go.lighten()
        elif go.is_light:
            go.darken()

        if exit.is_on():
            exit.lighten()
        elif exit.is_light:
            exit.darken()

        # letting go of drawing, now computing regression
        if not hold and arrived != [] and not smooth:
            if order[left_prop] - order[right_prop] == 0:
                wb1.calc_reg('none')
            elif order[left_prop] - order[right_prop] == -1:
                wb1.calc_reg('dev')
            else:
                wb1.calc_reg('int')

            arrived = wb1.compute_opt()
            arrived_2 = wb1.compute_pd_opt(wb2)

            # remove all out of range values that might come from regression
            l = len(arrived)
            for i in range(l):
                if not wb1.y + 25 < arrived[l - i - 1][1] < wb1.y + wb1.h - 25:
                    arrived.pop(l - i - 1)

            l = len(arrived_2)

            for i in range(l):
                if not wb2.y + 25 < arrived_2[l - i - 1][1] < wb2.y + wb2.h - 25:
                    arrived_2.pop(l - i - 1)
                elif not wb2.x + 25 < arrived_2[l - i - 1][0] < wb2.x + wb2.w - 25:
                    arrived_2.pop(l - i - 1)

            l = len(arrived_2)

            # third comb to eliminate discontinuities
            for i in range(l-1):
                if arrived_2[i+1][0]-arrived_2[i][0] > 2: # ensure x gaps are small
                    arrived_2 = arrived_2[:i]
                    break

            smooth = True

        # Updating Sprites
        if start:
            if not car.update(arrived_2): # drive the car
                if flag_received:
                    streak += star_1_received + star_2_received + star_3_received
                    print(streak)
                else:
                    streak = 0
                    lose.play()

                arrived = []
                arrived_2 = []
                wb1.clear()
                car.clear()
                star_1.clear()
                star_2.clear()
                star_3.clear()
                flag.clear()

                smooth = False
                start = False
                star_1_received = False
                star_2_received = False
                star_3_received = False
                flag_received   = False

                star_cords = [[randint(450, 590), randint(70, 250)], [randint(450, 590), randint(70, 250)],
                              [randint(450, 590),
                               randint(70, 250)]]
                flag_cord = [600, randint(70, 250)]
                left_prop, right_prop = possibilities[randint(0, 3)]

                star_1 = Collideable(star_cords[0][0], star_cords[0][1], 52, 52, star)
                star_2 = Collideable(star_cords[1][0], star_cords[1][1], 52, 52, star)
                star_3 = Collideable(star_cords[2][0], star_cords[2][1], 52, 52, star)
                flag = Collideable(flag_cord[0], flag_cord[1], 86, 100, flag_i)

                if streak > high_score:
                    high_score = streak
                    np.save('high_score.npy', np.array([streak]))
                    if streak >= 100:
                        car = Car(wb2.x, wb2.y + wb2.h/2, 64, 48, pygame.image.load('Assets/car_g.png'))

                for x in range(30):
                    pygame.display.flip()
                    clock.tick(60)

        # check collisions
        if pygame.sprite.collide_mask(car, star_1) and not star_1_received:
            collect_star.play()
            star_1_received = True

        if pygame.sprite.collide_mask(car, star_2) and not star_2_received:
            collect_star.play()
            star_2_received = True

        if pygame.sprite.collide_mask(car, star_3) and not star_3_received:
            collect_star.play()
            star_3_received = True

        if pygame.sprite.collide_mask(car, flag) and not flag_received:
            collect_flag.play()
            flag_received = True

        if star_1_received:
            star_1.pop()

        if star_2_received:
            star_2.pop()

        if star_3_received:
            star_3.pop()

        if flag_received:
            flag.pop()

        # Drawing
        screen.fill('white')
        screen.blit(back, (-20, -20))
        render(eraser)
        render(go)
        render(exit)
        render(wb1)
        render(wb2)

        if len(arrived) > 1:
            pygame.draw.lines(screen, 'black', False, arrived, 4)

        if len(arrived_2) > 1:
            pygame.draw.lines(screen, (150, 150, 150), False, arrived_2, 4)

        render(star_1)
        render(star_2)
        render(star_3)
        render(flag)
        render(car)

        screen.blit(lhs_label, (wb1.x + wb1.w/2 - 13, 40))
        screen.blit(rhs_label, (wb2.x + wb2.w / 2 - 13, 40))
        screen.blit(fct_label, (350, 450))
        screen.blit(stk_label, (350, 365))
        screen.blit(hsr_label, (350, 405))

        # if exit has been pressed:
        if leave:
            break

        # Updating the window
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    bg_music = pygame.mixer.Sound('Assets/background_music.mp3')
    bg_music.set_volume(0.7)
    bg_music.play(-1)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Game')
    game_start()