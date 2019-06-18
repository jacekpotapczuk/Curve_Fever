import pygame as pg
import const as c
import random
from timeit import default_timer as timer
import importlib
from Player import Player
from Settings import Settings


class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((c.RES_X, c.RES_Y))
        self.clock = pg.time.Clock()
        pg.font.init()
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.playing = False  # is game still running (single match)
        self.running = True  # is whole window supposed to run
        self.isBegining = True  # is begining (you can't die in begining)
        self.players = []
        self.time = timer()

    def new(self):
        """
        Start new game
        :return: None
        """
        self.isBegining = True
        self.time = timer()
        self.players = []
        self.time = timer()
        importlib.reload(c)  # reload game settings
        for i in range(c.NUM_PLAYERS):
            self.players.append(Player(random.uniform(0.0, c.RES_X/2.0) + c.RES_X/4.0, random.uniform(0.0, c.RES_Y/2.0) + c.RES_Y/4.0, c.PLAYER_SPEED, c.PLAYER_SPEED, random.uniform(0, 2*c.PI), c.PLAYER_SIZE, c.PLAYERS_COLOR[i], 0, 0, c.PLAYER_SIZE, False, timer(), timer(), c.PLAYERS_KEY[i][0], c.PLAYERS_KEY[i][1]))
        self.run()

    def run(self):
        """
        main game loop
        :return: None
        """
        self.playing = True
        while self.playing:
            self.clock.tick(c.GAME_FPS)
            self.events()
            pg.display.update()
            self.draw()
        self.show_end_screen()

    def events(self):
        """
        handle events
        :return: None
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

        if timer() - self.time > 3.0:  # if more than 3s from start of the game
            self.isBegining = False

        dt = self.clock.tick(c.GAME_FPS) / 100
        for player in self.players:
            player.on_break()
            self.wrap_coordinates(player)
            player.move(dt)
            if not self.isBegining:
                if player.is_collision(self.window):
                    player.dx = 0.0
                    player.dy = 0.0
                    player.is_alive = False

        # check if only one player is left
        dead_players = 0
        for player in self.players:
            if not player.is_alive:
                dead_players += 1
        if dead_players == len(self.players) - 1:
            self.playing = False

    def draw(self):
        """
        Draw everything on screen
        :return: None
        """
        if self.isBegining:
            self.window.fill(c.BLACK)
        else:
            pg.draw.rect(self.window, c.DARK_CYAN, pg.Rect(0, 0, c.RES_X, c.RES_Y), 10)

        for player in self.players:
            if player.isBreak:
                pg.draw.circle(self.window, c.BLACK, (int(player.xh), int(player.yh)), player.sizeh)
            pg.draw.circle(self.window, player.color, (int(player.x), int(player.y)), player.size)

    def show_start_screen(self):
        """
        handles start screen
        :return: None
        """
        settings_icon_30_30 = pg.image.load("img\\settings_30_30.png")
        exit_icon_25_25 = pg.image.load("img\\exit_25_25.png")
        font2 = pg.font.SysFont('Comic Sans MS', 18)
        font3 = pg.font.SysFont('Comic Sans MS', 55)
        title = font3.render('Curve Fever', False, c.RED)
        author = font2.render('Author: Jacek Potapczuk', False, c.YELLOW)

        settings = Settings(self.window, c.RES_X - 350, 0, 320, 170, exit_icon_25_25)
        while True:
            self.clock.tick(c.MENU_FPS)
            self.window.fill(c.BLACK)
            mouse_pos = pg.mouse.get_pos()
            mouse_click = pg.mouse.get_pressed()
            if mouse_pos[0] > c.RES_X - 25 and mouse_pos[1] < 25:
                self.window.blit(settings_icon_30_30, (c.RES_X - 30, 0))

                if mouse_click[0] == 1:
                    settings.show = True
            else:
                self.window.blit(pg.transform.scale(settings_icon_30_30, (25, 25)), (c.RES_X - 25, 0))
                if mouse_click[0] == 1 and c.RES_X - 30 > mouse_pos[0] > c.RES_X - 55 and mouse_pos[1] < 25:
                    settings.show = False

            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                if settings.show:
                    settings.show = False
                else:
                    self.running = False
                    break
            if keys[pg.K_SPACE]:
                break

            self.window.blit(title, (c.RES_X / 2 - title.get_width()/2, c.RES_Y / 4 - title.get_height()/2))
            self.window.blit(author, (c.RES_X - 250, c.RES_Y - 50))

            if c.RES_X / 2 - 50 <= mouse_pos[0] <= c.RES_X / 2 - 50 + 100 and c.RES_Y / 1.45 - c.RES_Y / 7 + 5 <= mouse_pos[1] <= c.RES_Y / 1.45 - c.RES_Y / 7 + 5 + 40:
                pg.draw.rect(self.window, c.GREEN, pg.Rect(c.RES_X / 2 - 50, c.RES_Y / 1.45 - c.RES_Y / 7 + 5, 100, 40), 0)
                if mouse_click[0] == 1:
                    break
            else:
                pg.draw.rect(self.window, c.DARK_GREEN, pg.Rect(c.RES_X / 2 - 50, c.RES_Y / 1.45 - c.RES_Y / 7 + 5, 100, 40), 0)

            self.window.blit(self.font.render('Start', False, c.WHITE), (c.RES_X / 2 - 50 + 10, c.RES_Y / 1.45 - c.RES_Y / 7))
            settings.update(mouse_pos, mouse_click)

            pg.display.update()
            pg.event.pump()
        self.new()

    def show_end_screen(self):
        """
        handle end screen
        :return: None
        """
        textsurface = self.font.render('Error', False, c.WHITE)
        for player in self.players:
            print(player.is_alive)
            if player.is_alive:
                textsurface = self.font.render('{} player won'.format(c.COLOR_DICT[player.color]), False, c.WHITE)
                break

        self.window.blit(textsurface, (c.RES_X/2 - textsurface.get_width()/2, c.RES_Y/4 - textsurface.get_height()))

        while not self.playing:
            self.clock.tick(c.GAME_FPS)
            mouse_pos = pg.mouse.get_pos()
            mouse_click = pg.mouse.get_pressed()
            if (c.RES_X - 220) / 2 - 50 <= mouse_pos[0] <= (c.RES_X - 220) / 2 - 50 + 150 and c.RES_Y / 2 - c.RES_Y / 6 + 100 <= mouse_pos[1] <= c.RES_Y / 2 - c.RES_Y / 6 + 100 + 100:
                pg.draw.rect(self.window, c.GREY, pg.Rect((c.RES_X - 220) / 2 - 50, c.RES_Y / 2 - c.RES_Y / 6 + 100, 150, 40))
                if mouse_click[0] == 1:
                    self.new()
            else:
                pg.draw.rect(self.window, c.DARK_GREY, pg.Rect((c.RES_X - 220) / 2 - 50, c.RES_Y / 2 - c.RES_Y / 6 + 100, 150, 40))

            if (c.RES_X - 220) / 2 + 140 <= mouse_pos[0] <= (c.RES_X - 220) / 2 + 140 + 150 and c.RES_Y / 2 - c.RES_Y / 6 + 100 <= mouse_pos[1] <= c.RES_Y / 2 - c.RES_Y / 6 + 100 + 150:
                pg.draw.rect(self.window, c.GREY, pg.Rect((c.RES_X - 220) / 2 + 140, c.RES_Y / 2 - c.RES_Y / 6 + 100, 150, 40))
                if mouse_click[0] == 1:
                    self.show_start_screen()
            else:
                pg.draw.rect(self.window, c.DARK_GREY, pg.Rect((c.RES_X - 220) / 2 + 140, c.RES_Y / 2 - c.RES_Y / 6 + 100, 150, 40))

            textsurface2 = self.font.render("RESTART", False, c.WHITE)
            self.window.blit(textsurface2, ((c.RES_X - 220) / 2 - 50 + 3, c.RES_Y / 2 - c.RES_Y / 6 + 100 - 5))
            textsurface3 = self.font.render("MENU", False, c.WHITE)
            self.window.blit(textsurface3, ((c.RES_X - 220) / 2 + 140 + 3 + 25, c.RES_Y / 2 - c.RES_Y / 6 + 100 - 5))

            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                self.running = False
                self.playing = True  # to leave loop
            if keys[pg.K_SPACE]:
                self.playing = True
                self.running = True
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = True
                    self.running = False

            pg.display.update()

    def wrap_coordinates(self, player):
        """
        wraps coordinates of players so they can't go outside of map
        :param player: Player
        :return: None
        """
        player.x = player.x + c.RES_X if player.x < 0.0 else player.x
        player.x = player.x - c.RES_X if player.x >= c.RES_X else player.x
        player.y = player.y + c.RES_Y if player.y < 0.0 else player.y
        player.y = player.y - c.RES_Y if player.y >= c.RES_Y else player.y


g = Game()
g.show_start_screen()
while g.running:
    g.new()

pg.quit()
