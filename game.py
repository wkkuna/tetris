import pygame
import random
import time
import os
from pygame.locals import *


class Tetromino:
    # The Tetronimos and their rotations are described as
    # coordiantes of 1x1 squares they're made of on 4x4 square
    tetrominos = [
        # "I"
        [
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(0, 0), (0, 1), (0, 2), (0, 3)]
        ],
        # "Z"
        [
            [(0, 0), (0, 1), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (1, 0), (2, 0)]
        ],
        # "S"
        [
            [(0, 1), (0, 2), (1, 0), (1, 1)],
            [(0, 0), (1, 0), (1, 1), (2, 1)]
        ],
        # "J"
        [
            [(0, 1), (0, 2), (1, 1), (2, 1)],
            [(0, 0), (0, 1), (0, 2), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 0)],
            [(0, 0), (1, 0), (1, 1), (1, 2)]
        ],
        # "L"
        [
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 0), (1, 1), (1, 2)],
            [(0, 0), (1, 0), (2, 0), (2, 1)],
            [(0, 0), (0, 1), (0, 2), (1, 0)]
        ],
        # "T"
        [
            [(0, 0), (0, 1), (0, 2), (1, 1)],
            [(0, 1), (1, 0), (1, 1), (2, 1)],
            [(0, 1), (1, 0), (1, 1), (1, 2)],
            [(0, 0), (1, 0), (1, 1), (2, 0)],
        ],
        # "O"
        [
            [(0, 0), (0, 1), (1, 0), (1, 1)]
        ],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.tetrominos) - 1)
        self.rotation = 0
        self.color = (255, 182, 192)

    def rotate_left(self):
        self.rotation = (self.rotation - 1) % len(self.tetrominos[self.type])

    def rotate_right(self):
        self.rotation = (self.rotation + 1) % len(self.tetrominos[self.type])

    def get(self):
        return self.tetrominos[self.type][self.rotation]


BG_C = (250, 250, 250)
GRID_C = (100, 100, 100)


class Color:
    # https://coolors.co/palette/fbf8cc-fde4cf-ffcfd2-f1c0e8-cfbaf0-a3c4f3-90dbf4-8eecf5-98f5e1-b9fbc0
    colors = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "grey": (192, 192, 192),
        "pink": (255, 182, 192),
        "yellow": (251, 248, 204),
        "orange": (253, 228, 207),
        "rose": (255, 207, 210),
        "pink2": (241, 192, 232),
        "purple": (207, 186, 240),
        "blue": (163, 196, 243),
        "blue2": (144, 219, 244),
        "light_blue": (142, 236, 245),
        "light_green": (152, 245, 225),
        "green": (185, 251, 192)
    }

    def __init__(self):
        pass

    def get(self, color):
        return self.colors[color]


class Theme:
    def __init__(self):
        pass


class GridField:
    def __init__(
        self,
        width_px, height_px,
        block_size,
        off_l=0, off_r=0,
        off_u=0, off_d=0
    ):
        self.width = (width_px - off_l - off_r) // block_size
        self.height = (height_px - off_u - off_d) // block_size + 1
        self.height_px = height_px
        self.width_px = width_px
        self.off_l = off_l
        self.off_r = off_r
        self.off_u = off_u
        self.off_d = off_d
        self.block_size = block_size

        print("Size: {} x {}".format(self.width, self.height))
        new_field = []
        for _ in range(0, self.height):
            new_field.append([0] * (self.width))

        self.field = new_field

    def get_elem(self, x, y):
        return self.field[y][x]

    def set_elem(self, x, y, val):
        self.field[y][x] = val

    def is_empty(self, x, y):
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return False
        return self.field[y][x] == 0

    def draw(self, window):
        for y in range(self.off_u, self.height_px - self.off_d, self.block_size):
            for x in range(self.off_l, self.width_px - self.off_r, self.block_size):
                xidx = (x - self.off_l) // self.block_size
                yidx = (y - self.off_u) // self.block_size

                if self.is_empty(xidx, yidx):
                    c = Color().get("white")
                else:
                    c = self.get_elem(xidx, yidx)

                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                pygame.draw.rect(window, c, rect)
                pygame.draw.rect(window, Color().get("black"), rect, 1)

    def draw_tetronimo(self, window, tet):
        squares = tet.get()
        for (sy, sx) in squares:
            rect = pygame.Rect((tet.x + sx) * self.block_size + self.off_l, (tet.y + sy)
                               * self.block_size + self.off_u, self.block_size, self.block_size)
            pygame.draw.rect(window, tet.color, rect)
            pygame.draw.rect(window, Color().get("black"), rect, 1)

    def clear_line(self, idx):
        self.field.remove(self.field[idx])

    def insert_line(self, idx, line):
        self.field.insert(idx, line)

    def clear(self):
        self.field = []
        for y in range(0, self.height):
            self.field.append([0] * (self.width))


class Screen:
    game = []
    hold = []
    queue = []
    window = None

    def __init__(self, width, height, block_size):
        print(width, height)
        self.window = pygame.display.set_mode((width, height))
        self.block_size = block_size

        self.game = GridField(width, height, block_size, int(width*(1/4)),
                              int(width*(1/4)), int(height*(5/80)), int(height*(5/80)))

        self.hold = GridField(width, height, block_size, block_size,
                              int(width * (3/4)) + block_size, int(height*(1/5)), int(height*(4/5)) - block_size*6)

        self.queue = GridField(width, height, block_size, int(width * (3/4)) + block_size,
                               block_size, int(height*(5/80)), int(height*(75/80) - block_size*15))

    def is_empty(self, x, y):
        if x >= self.game.width or x < 0 or y >= self.game.height or y < 0:
            return False

        return self.game.get_elem(x, y) == 0

    def try_update(self, T):
        squares = T.get()
        for (sy, sx) in squares:
            (x, y) = (sx + T.x, sy + T.y)
            if x < 0 or x >= self.game.width or y < 0 or y >= self.game.height:
                return False

        for (sy, sx) in squares:
            (x, y) = (sx + T.x, sy + T.y)
            self.game.set_elem(x, y, T.color)
        return True

    def clear_lines(self):
        lines = []
        height = self.game.height
        width = self.game.width

        for y in range(0, height):
            square_count = 0
            for x in range(0, width):
                if not self.game.is_empty(x, y):
                    square_count += 1
            if square_count == width:
                lines.append(y)

        for line in lines:
            self.game.clear_line(line)

        for line in lines:
            self.game.insert_line(0, [0] * (width))

        return len(lines)

    def update_hold(self, T):
        squares = T.get()
        self.hold.clear()
        for (sy, sx) in squares:
            (x, y) = (sx, sy + 1)
            self.hold.set_elem(x, y, Color().get("orange"))

    def update_queue(self, queue):
        self.queue.clear()
        ty = 1
        ty_n = ty
        for i, T in enumerate(queue):
            for (sy, sx) in T.get():
                (x, y) = (sx, sy + ty)
                ty_n = max(ty_n, y)
                self.queue.set_elem(x, y, Color().get("blue"))
            ty = ty_n + 2

    def draw(self, tet, s):
        self.window.fill(Color().get("white"))
        self.game.draw(self.window)
        self.game.draw_tetronimo(self.window, tet)
        self.queue.draw(self.window)
        self.hold.draw(self.window)
        pygame.display.set_caption("Tetris")
        score = pygame.font.SysFont("Helvetica", 25)
        score_txt = score.render(
            "Score: " + str(s), True, Color().get("black"))
        self.window.blit(score_txt, (self.block_size, self.block_size))


class Tetris:
    level = 0
    speed = 50
    score = 0
    state = "initial"
    S = None
    curr_tetromino = None
    held_tetromino = None
    queue = []
    clock = None
    fps = 30

    def __init__(self, width, height):
        self.S = Screen(width, height, 40)
        self.width = width
        self.height = height
        for i in range(0, 3):
            self.queue.append(Tetromino(0, 0))

        self.new_tetromino()
        self.clock = pygame.time.Clock()

    def new_tetromino(self):
        self.curr_tetromino = self.queue[0]
        self.queue.remove(self.curr_tetromino)
        self.curr_tetromino.x = 3
        self.curr_tetromino.y = 0
        self.queue.append(Tetromino(0, 0))
        self.S.update_queue(self.queue)

    def allowed_layout(self):
        squares = self.curr_tetromino.get()
        for (sy, sx) in squares:
            if not self.S.is_empty(sx + self.curr_tetromino.x, sy + self.curr_tetromino.y):
                return False
        return True

    def count_lines(self):
        self.score += self.S.clear_lines()
        print("Score {}".format(self.score))

    def lock(self):
        updated = self.S.try_update(self.curr_tetromino)
        self.count_lines()
        if not updated:
            self.state = "over"
        self.new_tetromino()

    def move(self, direction):
        moves = {
            "down": (0, 1, True),
            "left": (-1, 0, False),
            "right": (1, 0, False)
        }

        (x, y, lock) = moves[direction]
        self.curr_tetromino.x += x
        self.curr_tetromino.y += y
        if not self.allowed_layout():
            self.curr_tetromino.x -= x
            self.curr_tetromino.y -= y
            if lock:
                self.lock()

    # Quickly drop tetromino
    def drop(self):
        while self.allowed_layout():
            self.curr_tetromino.y += 1
        self.curr_tetromino.y -= 1
        self.lock()

    # Save tetromino on a side
    def hold(self):
        if self.held_tetromino == None:
            self.held_tetromino = self.curr_tetromino
            self.new_tetromino()
        else:
            tmp = self.held_tetromino
            self.held_tetromino = self.curr_tetromino
            self.curr_tetromino = tmp

        self.held_tetromino.rotation = 0
        self.curr_tetromino.x = 3
        self.curr_tetromino.y = 0
        self.S.update_hold(self.held_tetromino)

    def set_state(self, new_state):
        self.state = new_state

    def rotate(self):
        self.curr_tetromino.rotate_right()
        if not self.allowed_layout():
            self.curr_tetromino.rotate_left()

    def draw_game(self):
        self.S.draw(self.curr_tetromino, self.score)

    def reset(self):
        self.level = 0
        self.score = 0
        self.state = "initial"
        self.curr_tetromino = None
        self.held_tetromino = None
        self.queue = []

        self.S.hold.clear()
        self.S.queue.clear()
        self.S.game.clear()

        for i in range(0, 3):
            self.queue.append(Tetromino(0, 0))

        self.new_tetromino()

    # Main Menu

    def main_menu(self):
        def text_format(message, textFont, textSize, textColor):
            newFont = pygame.font.SysFont(textFont, textSize, bold=True)
            newText = newFont.render(message, True, textColor)
            return newText

        class Option:
            options = {
                0: "new_game",
                1: "resume",
                2: "quit"
            }

            def __init__(self, opt):
                self.option = opt

            def next(self):
                if self.option == "new_game":
                    self.option = "resume"
                elif self.option == "resume":
                    self.option = "quit"

            def prev(self):
                if self.option == "resume":
                    self.option = "new_game"
                elif self.option == "quit":
                    self.option = "resume"

            def get(self):
                return self.option

            def getTextColor(self, option):
                if option == self.option:
                    return Color().get("white")
                return Color().get("black")

        # Game Fonts
        font = "Helvetica"

        menu = True
        selected = Option("new_game")
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected.prev()
                        if selected.get() == "resume" and self.state == "initial":
                            selected.prev()
                    elif event.key == pygame.K_DOWN:
                        selected.next()
                        if selected.get() == "resume" and self.state == "initial":
                            selected.next()
                    if event.key == pygame.K_RETURN:
                        if selected.get() == "new_game":
                            self.reset()
                            return
                        if selected.get() == "resume" and self.state != "initial":
                            return
                        if selected.get() == "quit":
                            pygame.quit()
                            quit()
                    if event.key == pygame.K_ESCAPE and self.state != "initial":
                        self.reset()
                        return

            # Main Menu UI
            s = pygame.Surface((self.width, self.height))
            s.set_alpha(10)
            s.fill(Color().get("blue"))
            self.S.window.blit(s, (0, 0))

            color_resume = selected.getTextColor("resume")
            color_new_game = selected.getTextColor("new_game")
            color_quit = selected.getTextColor("quit")

            if self.state == "initial":
                color_resume = Color().get("grey")

            title = text_format("Tetris", font, 90, Color().get("yellow"))

            text_new_game = text_format("NEW GAME", font, 75, color_new_game)
            text_quit = text_format("QUIT", font, 75, color_quit)
            text_resume = text_format("RESUME", font, 75, color_resume)

            title_rect = title.get_rect()
            new_game_rect = text_new_game.get_rect()
            resume_rect = text_resume.get_rect()
            quit_rect = text_quit.get_rect()

            # Main Menu Text
            self.S.window.blit(title, (self.width/2 - (title_rect[2]/2), 80))
            self.S.window.blit(
                text_new_game, (self.width/2 - (new_game_rect[2]/2), 300))
            self.S.window.blit(
                text_resume, (self.width/2 - (resume_rect[2]/2), 400))
            self.S.window.blit(
                text_quit, (self.width/2 - (quit_rect[2]/2), 500))
            pygame.display.update()
            self.clock.tick(self.fps)

    def run(self):
        def current_milli_time():
            return round(time.time() * 1000)

        self.clock
        last_time = 0
        interval = 65
        loop = 0

        self.main_menu()
        while self.state != "over":
            self.draw_game()

            keys = pygame.key.get_pressed()

            if current_milli_time() > last_time + interval:
                if keys[pygame.K_DOWN]:
                    self.move("down")
                if keys[pygame.K_LEFT]:
                    self.move("left")
                if keys[pygame.K_RIGHT]:
                    self.move("right")

                last_time = current_milli_time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.set_state("over")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.rotate()
                    if event.key == pygame.K_SPACE:
                        self.drop()
                    if event.key == pygame.K_c:
                        self.hold()
                    if event.key == pygame.K_ESCAPE:
                        self.set_state("pause")
                        self.main_menu()

            if loop == self.speed:
                self.move("down")
                loop = 0
            loop += 1

            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()


H = 1000
W = 800
pygame.init()
T = Tetris(W, H)
T.run()
