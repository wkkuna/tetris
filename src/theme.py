import pygame


class Color:
    colors = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "grey": (192, 192, 192),
        "pink": (255, 182, 192),
        # https://coolors.co/palette/fbf8cc-fde4cf-ffcfd2-f1c0e8-cfbaf0-a3c4f3-90dbf4-8eecf5-98f5e1-b9fbc0
        "FBF8CC": (251, 248, 204),
        "FDE4CF": (253, 228, 207),
        "FFCFD2": (255, 207, 210),
        "F1C0E8": (241, 192, 232),
        "CFBAF0": (207, 186, 240),
        "A3C4F3": (163, 196, 243),
        "90DBF4": (144, 219, 244),
        "8EECF5": (142, 236, 245),
        "98F5E1": (152, 245, 225),
        "B9FBC0": (185, 251, 192),
        # https://coolors.co/9aadbf-6d98ba-d3b99f-c17767-210203-7a542e-2a2e45-5c0029
        "9AADBF": (154, 173, 191),
        "6D98BA": (109, 152, 186),
        "D3B99F": (211, 185, 159),
        "C17767": (193, 119, 103),
        "210203": (33, 2, 3),
        "7A542E": (122, 84, 46),
        "2A2E45": (42, 46, 69),
        "5C0029": (92, 0, 41),
        "713D35": (113, 61, 53),
        "7A5E51": (122, 94, 81),
        "431737": (67, 23, 55),
        # greys
        "D3D3D3": (211, 211, 211),
        "848884": (132, 136, 132),
    }

    def __init__(self):
        pass

    def get(self, color):
        return self.colors[color]


class Theme:
    color_sets = [
        # default set
        {
            0: "FBF8CC",
            1: "FDE4CF",
            2: "FFCFD2",
            3: "F1C0E8",
            4: "CFBAF0",
            5: "90DBF4",
            6: "B9FBC0",
            7: "D3D3D3",    # ghost piece
            8: "white",     # bg
            9: "A3C4F3",    # menu
            10: "black",     # text color
            11: "white",     # text color active
            12: "grey",      # text color blocked
        },
        # dark set
        {
            0: "431737",
            1: "6D98BA",
            2: "D3B99F",
            3: "C17767",
            4: "7A542E",
            5: "2A2E45",
            6: "5C0029",
            7: "848884",     # ghost piece
            8: "210203",     # bg
            9: "7A5E51",     # menu
            10: "D3B99F",     # text color
            11: "white",      # text color active
            12: "grey",       # text color blocked
        }
    ]

    def __init__(self, font, s=0):
        self.color_set = self.color_sets[s]
        self.font = font

    def get_tet_color(self, T_type):
        return Color().get(self.color_set[T_type])

    def get_bg_color(self):
        return Color().get(self.color_set[8])

    def get_menu_color(self):
        return Color().get(self.color_set[9])

    def get_font(self):
        return self.font

    def get_text_color(self, active=False, blocked=False):

        if active:
            c = self.color_set[11]
        else:
            c = self.color_set[10]

        if blocked:
            c = self.color_set[12]

        return Color().get(c)

    def text_format(self, message, textSize, textColor, bold):
        newFont = pygame.font.SysFont(self.font, textSize, bold)
        newText = newFont.render(message, True, textColor)
        return newText
