from talon import actions
from .utils import get_screen

class Position:
    def left(self):
        screen = get_screen()
        actions.mouse_move(screen.x + 200, screen.y + screen.height / 2)

    def main(self):
        screen = get_screen()
        actions.mouse_move(screen.x + screen.width * .4, screen.y + screen.height / 2)

    def down(self):
        screen = get_screen()
        actions.mouse_move(screen.width / 2, screen.height - 150)

    def right(self):
        screen = get_screen()
        actions.mouse_move(screen.width - 200, screen.y + screen.height / 2)

    def up(self):
        screen = get_screen()
        actions.mouse_move(screen.width / 2, screen.y + 50)

position = Position()