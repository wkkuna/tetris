import pygame
import math
import time
from pygame.locals import *
from src.menu import *
from src.screen import *
from src.tetronimo import *
import src.theme as T
from copy import copy


class Level:
    def get(self, score):
        if score == 0:
            return 1
        return int(math.log(score, 2) + 1)


class Tetris:
    level = 1
    speed = 50
    score = 0
    state = "initial"
    S = None
    curr_tetromino = None
    held_tetromino = None
    ghost_piece = None
    queue = []
    clock = None
    fps = 25

    def __init__(self, width, height, theme=0):
        pygame.init()
        options = {
            0: "new game",
            1: "resume",
            2: "quit"
        }
        self.menu = Menu(options)
        self.theme = T.Theme("Helvetica", theme)
        self.block_size = 40
        self.S = Screen(width, height, self.block_size, self.theme)
        for i in range(0, 3):
            self.queue.append(Tetromino(3, 0, self.theme))

        self.new_tetromino()
        self.clock = pygame.time.Clock()

    def new_tetromino(self):
        self.curr_tetromino = self.queue[0]
        self.queue.remove(self.curr_tetromino)
        self.queue.append(Tetromino(3, 0, self.theme))
        self.S.update_queue(self.queue)
        self.update_ghost()
        if not self.allowed_layout(self.curr_tetromino):
            self.gameover()

    def allowed_layout(self, t):
        squares = t.get()
        for (sy, sx) in squares:
            if not self.S.is_empty(sx + t.x, sy + t.y):
                return False
        return True

    def update_ghost(self):
        m_y = 0
        self.ghost_piece = copy(self.curr_tetromino)
        self.ghost_piece.color = self.theme.get_tet_color(7)

        for (sy, sx) in self.curr_tetromino.get():
            m_y = max(m_y, sy + self.curr_tetromino.y)
            if m_y + sy >= self.S.game.height:
                my_y = self.S.game.height - sy

        while self.allowed_layout(self.ghost_piece):
            self.ghost_piece.y += 1
        self.ghost_piece.y -= 1

        self.ghost_piece.y = max(self.ghost_piece.y, 0)

    def levelup(self, level):
        diff = level - self.level
        if self.speed < 25:
            self.speed = max(self.speed - 2*diff, 2)
        else:
            self.speed = max(self.speed - 5*diff, 2)
        self.level = level

    def count_lines(self):
        self.score += (self.S.clear_lines() ** 2) * self.level
        new_level = Level().get(self.score)
        if self.level != new_level:
            self.levelup(new_level)

    def lock(self):
        updated = self.S.try_update(self.curr_tetromino)
        self.count_lines()
        if not updated:
            self.gameover()
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
        if not self.allowed_layout(self.curr_tetromino):
            self.curr_tetromino.x -= x
            self.curr_tetromino.y -= y
            if lock:
                self.lock()
        self.update_ghost()

    # Quickly drop tetromino
    def drop(self):
        while self.allowed_layout(self.curr_tetromino):
            self.curr_tetromino.y += 1
        self.curr_tetromino.y -= 1
        self.update_ghost()
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
        self.update_ghost()

    def set_state(self, new_state):
        self.state = new_state

    def rotate(self):
        self.curr_tetromino.rotate_right()
        if not self.allowed_layout(self.curr_tetromino):
            if not self.S.try_shift(self.curr_tetromino):
                self.curr_tetromino.rotate_left()
        self.update_ghost()

    def draw_game(self):
        self.S.draw(self.curr_tetromino, self.ghost_piece,
                    self.score, self.level)

    def gameover(self):
        self.set_state("initial")
        self.main_menu()

    def reset(self):
        self.level = 1
        self.score = 0
        self.state = "initial"
        self.curr_tetromino = None
        self.held_tetromino = None
        self.ghost_piece = None
        self.queue = []

        self.S.hold.clear()
        self.S.queue.clear()
        self.S.game.clear()

        for i in range(0, 3):
            self.queue.append(Tetromino(3, 0, self.theme))

        self.new_tetromino()

    # Main Menu
    def main_menu(self):
        select = self.menu
        menu = True
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        select.prev()
                        if select.get() == "resume" and self.state == "initial":
                            select.prev()
                    elif event.key == pygame.K_DOWN:
                        select.next()
                        if select.get() == "resume" and self.state == "initial":
                            select.next()
                    if event.key == pygame.K_RETURN:
                        if select.get() == "new game":
                            self.reset()
                            return
                        if select.get() == "resume" and self.state != "initial":
                            return
                        if select.get() == "quit":
                            pygame.quit()
                            quit()
                    if event.key == pygame.K_ESCAPE and self.state != "initial":
                        self.reset()
                        return

            self.S.draw_menu(select, self.state)
            self.clock.tick(self.fps)

    def run(self):
        def current_milli_time():
            return round(time.time() * 1000)

        self.clock
        last_time = 0
        interval = 67
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

            if loop >= self.speed:
                self.move("down")
                loop = 0
            loop += 1

            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()
