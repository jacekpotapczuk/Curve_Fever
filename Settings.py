import const as c
import math
import pygame as pg


class Settings:
    def __init__(self, window, x, y, l, w, exit_icon):
        self.window = window
        self.x = x
        self.y = y
        self.l = l
        self.w = w
        self.exit_icon = exit_icon

        self.show = False
        self.font = pg.font.SysFont('Comic Sans MS', 18)

        self.turn_speed_slider = Slider(self.window, c.RES_X - 220, 20, 120, 20, c.GREEN, c.DARK_YELLOW, c.YELLOW, 10, "ANGLE_DIF", 0.03, 0.015)
        self.player_speed_slider = Slider(self.window, c.RES_X - 220, 50, 120, 20, c.GREEN, c.DARK_YELLOW, c.YELLOW, 10, "PLAYER_SPEED", 20.0, 10.0)

        self.setting1 = self.font.render('Turning speed', False, c.BLACK)
        self.setting2 = self.font.render('Player speed', False, c.BLACK)
        self.setting3 = self.font.render('Number of players', False, c.BLACK)

        self.radio_1 = RadioButton(self.window, True, c.RES_X - 170, 90, 7, c.RED, "NUM_PLAYERS")
        self.radio_2 = RadioButton(self.window, False, c.RES_X - 170, 115, 7, c.RED, "NUM_PLAYERS")

    def update(self, mouse_pos, mouse_click):
        """
        Controls elements of settings and updates values
        :param mouse_pos: tuple
        :param mouse_click: tuple
        :return: None
        """
        if self.show:
            pg.draw.rect(self.window, c.BLUE, pg.Rect(self.x, self.y, self.l, self.w))
            self.window.blit(self.exit_icon, (c.RES_X - 55, 0))
            self.turn_speed_slider.update(mouse_pos, mouse_click)
            self.player_speed_slider.update(mouse_pos, mouse_click)

            self.window.blit(self.setting1, (c.RES_X - 345, 15))
            self.window.blit(self.setting2, (c.RES_X - 345, 45))

            self.window.blit(self.setting3, (c.RES_X - 345, 75))

            self.window.blit(self.font.render('2', False, c.BLACK), (c.RES_X - 158, 76))
            self.window.blit(self.font.render('4', False, c.BLACK), (c.RES_X - 158, 101))

            self.radio_1.update(mouse_pos, mouse_click)
            if self.radio_1.is_clicked:
                self.radio_2.is_clicked = False
            else:
                self.radio_2.is_clicked = True
            self.radio_2.update(mouse_pos, mouse_click)
            if self.radio_2.is_clicked:
                self.radio_1.is_clicked = False
            else:
                self.radio_1.is_clicked = True

            if c.RES_X - 165 <= mouse_pos[0] <= c.RES_X - 65 and 130 <= mouse_pos[1] <= 150:
                pg.draw.rect(self.window, c.GREEN, pg.Rect(c.RES_X - 165, 130, 100, 20), 0)
            else:
                pg.draw.rect(self.window, c.DARK_GREEN, pg.Rect(c.RES_X - 165, 130, 100, 20), 0)

            self.window.blit(self.font.render('Zatwierdź', False, c.BLACK), (c.RES_X - 160, 127))

            if mouse_click[0] == 1 and c.RES_X - 165 <= mouse_pos[0] <= c.RES_X - 65 and 130 <= mouse_pos[1] <= 150:
                self.turn_speed_slider.set_param()
                self.player_speed_slider.set_param()
                if self.radio_1.is_clicked:
                    self.radio_1.set_param("2")
                else:
                    self.radio_1.set_param("4")
                self.show = False

    def save(self):
        """
        Saves parameters
        :return: None
        """
        self.turn_speed_slider.set_param()
        self.player_speed_slider.set_param()


class RadioButton:
    def __init__(self, window, is_clicked, x, y, r, color, param):
        self.window = window
        self.is_clicked = is_clicked
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.param = param

    def update(self, mouse_pos, mouse_click):
        """
        updates button value
        :param mouse_pos: tuple
        :param mouse_click: tuple
        :return: None
        """
        if mouse_click[0] == 1 and math.sqrt(((float(mouse_pos[0]) - self.x) ** 2 + (float(mouse_pos[1]) - self.y) ** 2)) < float(self.r):
            if self.is_clicked:
                self.is_clicked = False
            else:
                self.is_clicked = True
        self.draw()

    def draw(self):
        """
        Draws value on screen
        :return: None
        """
        if self.is_clicked:
            pg.draw.circle(self.window, self.color, (self.x, self.y), self.r, 0)
        else:
            pg.draw.circle(self.window, self.color, (self.x, self.y), self.r, 1)

    def set_param(self, param_value):
        """
        Saves parameters to txt file
        :param param_value: float
        :return: None
        """
        with open("settings.txt", "r") as f:
            filedata = f.read()
        settings = [_.split("=") for _ in filedata.split("\n")]
        for setting in settings:
            if len(setting) < 2:  # if blank line
                continue
            if setting[0] == self.param:

                setting[1] = param_value

        with open("settings.txt", "w") as f:
            for setting in settings:
                if len(setting) < 2:  # if blank line
                    continue
                f.write(setting[0] + "=" + setting[1] + "\n")


class Slider:
    def __init__(self, window, x, y, l, w, line_color, b_c_not_clicked, b_c_clicked, button_size, param, param_def, param_change):
        self.window = window
        self.x = x
        self.y = y
        self.l = l - 20
        self.w = w
        self.line_color = line_color
        self.b_c_not_clicked = b_c_not_clicked
        self.b_c_clicked = b_c_clicked
        self.button_size = button_size
        self.param = param
        self.param_def = param_def
        self.param_change = param_change

        self.b_x = float(x + self.l * 0.5)
        self.b_y = float(self.y + 0.5 * self.w)
        self.is_clicked = False
        self.value = 0  # from [-1, 1] range - indicades how much slider is moved to left or righ (1 means max to right)
        self.param_value = param_def

    def update(self, mouse_pos, mouse_click):
        """
        Upadtes value of slider
        :param mouse_pos: tuple
        :param mouse_click: tuple
        :return: None
        """
        if mouse_click[0] == 1 and math.sqrt(((float(mouse_pos[0]) - self.b_x)**2 + (float(mouse_pos[1]) - self.b_y)**2)) < float(self.button_size):
            self.is_clicked = True

        if mouse_click[0] == 0:
            self.is_clicked = False

        if self.is_clicked and self.x <= mouse_pos[0] <= self.x + self.l:
            self.b_x = mouse_pos[0]
            self.value = 1 - 2*((self.x + self.l - self.b_x)/self.l)
            self.param_value = self.param_def + self.value * self.param_change
        self.draw()

    def draw(self):
        """
        Draws settings window
        :return: None
        """
        pg.draw.rect(self.window, self.line_color, pg.Rect(self.x, self.b_y - 2, self.l, int(self.w / 4)))
        if self.is_clicked:
            pg.draw.circle(self.window, self.b_c_clicked, (int(self.b_x), int(self.b_y)), self.button_size)
        else:
            pg.draw.circle(self.window, self.b_c_not_clicked, (int(self.b_x), int(self.b_y)), self.button_size)

        textsurface = pg.font.SysFont('Comic Sans MS', 18).render(str(round(self.param_value, 3)), False, c.WHITE)
        self.window.blit(textsurface, (self.x + self.l + 10, self.y - 3))

    def set_param(self):
        """
        Saves parameters to txt file
        :return: None
        """
        with open("settings.txt", "r") as f:
            filedata = f.read()
        settings = [_.split("=") for _ in filedata.split("\n")]
        for setting in settings:
            if len(setting) < 2:  # if blank line
                continue
            if setting[0] == self.param:
                setting[1] = str(self.param_value)

        with open("settings.txt", "w") as f:
            for setting in settings:
                if len(setting) < 2:  # if blank line
                    continue
                f.write(setting[0] + "=" + setting[1] + "\n")
