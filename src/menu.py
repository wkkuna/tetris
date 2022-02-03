import src.theme as T


class Menu:
    options = {}

    def __init__(self, options):
        self.options = options
        self.selected = 0

    def next(self):
        if self.selected < len(self.options) - 1:
            self.selected += 1

    def prev(self):
        if self.selected > 0:
            self.selected -= 1

    def get(self):
        return self.options[self.selected]

    def getTextColor(self, option):
        color = "white" if option == self.options[self.selected] else "black"
        return T.Color().get(color)

    def getText(self, option):
        return option.upper()
