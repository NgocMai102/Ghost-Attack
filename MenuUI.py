import pygame
from object.data import *
from Gameplay import *


def run(runfile):
    with open(runfile, "r") as rnf:
        exec(rnf.read())


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = (
            WIDTH / 2 + 200,
            HEIGHT / 2 - 200,
        )
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -200

    def draw_cursor(self):
        pygame.draw.rect(
            self.game.display,
            (0, 0, 0),
            (self.cursor_rect.x + 95, self.cursor_rect.y - 20, 220, 40),
            2,
        )

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 40
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 80
        self.tutorialx, self.tutorialy = self.mid_w, self.mid_h + 120
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 160
        self.exitx, self.exity = self.mid_w, self.mid_h + 200
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(background, (0, 0))
            self.game.draw_text(
                "Main Menu",
                40,
                WIDTH / 2 + 200,
                HEIGHT / 2 - 20 - 200,
            )
            self.game.draw_text("Start Game", 30, self.startx, self.starty)
            self.game.draw_text("Options", 30, self.optionsx, self.optionsy)
            self.game.draw_text("Tutorial", 30, self.tutorialx, self.tutorialy)
            self.game.draw_text("Credits", 30, self.creditsx, self.creditsy)
            self.game.draw_text("Exit Game", 30, self.exitx, self.exity)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.tutorialx + self.offset, self.tutorialy)
                self.state = "Tutorial"
            elif self.state == "Tutorial":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "Exit"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "Exit"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
            elif self.state == "Tutorial":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.tutorialx + self.offset, self.tutorialy)
                self.state = "Tutorial"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
                run("Run_game.py")
            elif self.state == "Options":
                self.game.curr_menu = self.game.options
            elif self.state == "Tutorial":
                self.game.curr_menu = self.game.tutorial
            elif self.state == "Credits":
                self.game.curr_menu = self.game.credits
            elif self.state == "Exit":
                print("hello")
                self.game.curr_menu = self.game.exit
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Volume"
        self.volx, self.voly = (
            WIDTH / 2 - 20,
            HEIGHT / 2 - 20,
        )
        self.cursor_rect.midtop = (self.volx + self.offset / 2, self.voly)
        self.check_input()

    def display_menu(self):
        self.run_display = True
        self.volume = 1
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(background, (0, 0))
            self.game.draw_text(
                "Options",
                40,
                WIDTH / 2 - 20,
                HEIGHT / 2 - 90,
            )
            self.game.draw_text("Volume", 25, self.volx, self.voly)
            pygame.draw.rect(
                self.game.display,
                (0, 0, 0),
                (self.cursor_rect.x - 135, self.cursor_rect.y + 30, 500, 30),
                2,
            )
            pygame.draw.rect(
                self.game.display,
                (100, 100, 100),
                (
                    self.cursor_rect.x - 135 + 2,
                    self.cursor_rect.y + 30 + 2,
                    500 * self.volume - 4,
                    30 - 4,
                ),
            )
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            pass
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.volume <= 0.99:
            self.volume += 0.01
            pygame.mixer.music.set_volume(self.volume + 0.01)
        if keys[pygame.K_LEFT] and self.volume >= 0.01:
            self.volume -= 0.01
            pygame.mixer.music.set_volume(self.volume - 0.01)


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.blit(background, (0, 0))
            self.game.draw_text("Credits", 50, WIDTH / 2, HEIGHT / 2 - 110)
            self.game.draw_text(
                "Made by Mai",
                30,
                WIDTH / 2,
                HEIGHT / 2 - 40,
            )
            self.game.draw_text(
                "Donate: MB Bank",
                20,
                WIDTH / 2,
                HEIGHT / 2 + 10,
            )
            self.game.draw_text(
                "91022033107",
                20,
                WIDTH / 2,
                HEIGHT / 2 + 40,
            )
            self.game.draw_text(
                "Pham Thi Ngoc Mai",
                20,
                WIDTH / 2,
                HEIGHT / 2 + 70,
            )
            self.blit_screen()


class TutorialMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.blit(MenuTutorial, (0, 0))
            self.blit_screen()


class ExitGame(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.game_end()
            self.game.display.fill(self.game.WHITE)
            self.game.draw_text("Thanks for Playing!", 50, WIDTH / 2, HEIGHT / 2)
            self.game.window.blit(self.game.display, (0, 0))
            self.game.draw_text(
                "Press Enter to exit or Esc to return to Main Menu",
                40,
                WIDTH / 2,
                HEIGHT / 2 - 50,
            )
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
