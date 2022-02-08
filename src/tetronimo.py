import random


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

    def __init__(self, x, y, theme):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.tetrominos) - 1)
        self.rotation = 0
        self.theme = theme
        self.color = theme.get_tet_color(self.type)

    def __copy__(self):
        T = Tetromino(self.x, self.y, self.theme)
        T.type = self.type
        T.rotation = self.rotation
        T.color = self.color
        return T

    def rotate_left(self):
        self.rotation = (self.rotation - 1) % len(self.tetrominos[self.type])

    def rotate_right(self):
        self.rotation = (self.rotation + 1) % len(self.tetrominos[self.type])

    def shift(self, dx):
        self.x += dx

    def get(self):
        return self.tetrominos[self.type][self.rotation]
