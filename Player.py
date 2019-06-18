import random
from timeit import default_timer as timer
import const as c
import math
import pygame as pg


class Player:
    def __init__(self, x, y, dx, dy, angle, size, color, xh, yh, sizeh, isBreak, timeBreak, timeSafe, left, right):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.angle = angle
        self.size = size
        self.color = color
        self.xh = xh
        self.yh = yh
        self.sizeh = sizeh
        self.isBreak = isBreak
        self.timeBreak = timeBreak
        self.timeSafe = timeSafe
        self.left = left
        self.right = right
        self.is_alive = True
        self.time_start = timer()

    def move(self, dt):
        """
        Move player
        :param dt: float
        :return: None
        """
        keys = pg.key.get_pressed()
        if keys[self.left]:
            self.angle -= c.TURN_SPEED
        if keys[self.right]:
            self.angle += c.TURN_SPEED

        # keep angle in range -2pi to 2pi for simplicity
        self.angle = self.angle % (2 * c.PI)

        # save coordinates from last frame
        self.xh = self.x
        self.yh = self.y
        self.sizeh = self.size

        # actual move
        self.x += math.sin(self.angle) * self.dx * dt
        self.y += -math.cos(self.angle) * self.dy * dt

    def is_collision(self, window):
        """
        Check if collistion
        :param window: Surface
        :return: Bool
        """
        quadrant = 0
        if (0.0 <= self.angle < c.PI/2.0) or (-2.0 * c.PI < self.angle <= -(3.0/2.0) * c.PI):
            quadrant = 1
        elif (c.PI/2.0 <= self.angle < c.PI) or (-(3.0/2.0) * c.PI < self.angle <= -c.PI):
            quadrant = 2
        elif (c.PI <= self.angle < (3.0/2.0) * c.PI) or (-c.PI < self.angle <= - c.PI/2.0):
            quadrant = 3
        elif ((3.0/2.0) * c.PI <= self.angle < 2.0 * c.PI) or (- c.PI/2.0 < self.angle <= 0):
            quadrant = 4

        for x in range(int(self.x) - self.size, int(self.x) + self.size + 1):
            for y in range(int(self.y) - self.size, int(self.y) + self.size + 1):
                odl = math.sqrt((x - self.xh)**2 + (y - self.yh)**2)

                if x < 0 or x > c.RES_X or y < 0 or y > c.RES_Y:
                    return True
                if quadrant == 1:
                    if x < self.xh or y > self.yh:
                        odl = 0.0
                elif quadrant == 2:
                    if x < self.xh or y < self.yh:
                        odl = 0.0
                elif quadrant == 3:
                    if x > self.xh or y < self.yh:
                        odl = 0.0
                elif quadrant == 4:
                    if x > self.xh or y > self.yh:
                        odl = 0.0
                if self.sizeh + math.sqrt(self.sizeh) < odl:
                    if window.get_at((x, y)) != (0, 0, 0, 255):
                        print("Kolizja w ({},{})".format(x, y))
                        print("xh i yh to ({},{})".format(self.xh, self.yh))
                        print("cwiartka {}".format(quadrant))
                        print("kat {}".format(self.angle))
                        print("Odl {}".format(odl))
                        return True
        return False

    def on_break(self):
        """
        random chance to put player on break (stop drawing)
        :return:
        """

        if self.isBreak is True:
            duration = random.uniform(0, 0.2)
            if timer() - self.timeBreak > 0.35 + duration:
                self.isBreak = False
                self.timeSafe = timer()
        else:
            if timer() - self.timeSafe < 2.0:
                return True
            los = random.uniform(0, 1)

            if los < 0.005:
                self.isBreak = True
                self.timeBreak = timer()
        return True

    def get_score(self):
        """
        returns player score
        :return: float
        """
        return timer() - self.time_start
