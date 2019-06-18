import math
import pygame as pg

# changable settings

PLAYER_SPEED_DEFAULT = 20.0
PLAYER_SPEED = PLAYER_SPEED_DEFAULT
ANGLE_DIF_DEFAULT = 0.03  # turning angle
ANGLE_DIF = ANGLE_DIF_DEFAULT
PLAYERS_DEFAUL = 2
NUM_PLAYERS = PLAYERS_DEFAUL


# load settings from txt file

with open("settings.txt", "r") as f:
    for row in f:
        a = row.split("=")
        if a[0] == "ANGLE_DIF":
            ANGLE_DIF = float(a[1])
        elif a[0] == "PLAYER_SPEED":
            PLAYER_SPEED = float(a[1])
        elif a[0] == "NUM_PLAYERS":
            NUM_PLAYERS = int(a[1])


# unchangeable from game menu
RES_X = 500
RES_Y = 500
GAME_FPS = 120
MENU_FPS = 15
PI = math.pi
PLAYER_SIZE = 4

TURN_SPEED = 120/GAME_FPS * ANGLE_DIF

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (200, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
DARK_CYAN = (0, 139, 139)
YELLOW = (255, 255, 0)
DARK_YELLOW = (200, 200, 0)
GREY = (200, 200, 200)
DARK_GREY = (169, 169, 169)

PLAYERS_COLOR = [RED, BLUE, GREEN, YELLOW]
PLAYERS_KEY = [[pg.K_LEFT, pg.K_RIGHT],  [pg.K_a, pg.K_d], [pg.K_h, pg.K_k], [pg.K_KP1, pg.K_KP3]]
TITLE = "Curve"

COLOR_DICT = {(255, 255, 255): "WHITE", (0, 0, 0): BLACK, (255, 0, 0): "RED", (0, 0, 255): "BLUE",
              (255, 255, 0): "YELLOW", (0, 255, 0): "GREEN"}

