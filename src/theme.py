import pygame


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
    color_set = {}

    def __init__(self, tetrominos_color_set, font):
        if len(tetrominos_color_set) < 7:
            print("Invalid color set")
            raise
        self.color_set = tetrominos_color_set
        self.font = font

    def get_color(self, T_type):
        return Color().get(self.color_set[T_type])

    def get_font(self):
        return self.font

    def text_format(self, message, textSize, textColor, bold):
        newFont = pygame.font.SysFont(self.font, textSize, bold)
        newText = newFont.render(message, True, textColor)
        return newText
