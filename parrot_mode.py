from talon import Module, Context, actions, ctrl
from .src.scrolling import scrolling
from .src.tracking import tracking
from .src.movement import movement
from .src.cursor import cursor
from .src.position import position

mod = Module()
mod.mode("parrot_v6", "parrot mode v6")

ctx = Context()
ctx.matches = """
mode: user.parrot_v6
"""

parrot_mode_enabled = False

RED = "FF0000"
GREEN = "00FF00"
YELLOW = "FFFF00"
GREEN = "43e658"
TEAL = "34d5eb"

def move(dir: str):
    if not actions.user.parrot_config_mode() != "move":
        actions.user.parrot_v5_ui_cursor_yellow()
    movement.move(dir)

def stopper():
    cursor.color(RED)
    movement.stop()
    tracking.freeze()
    scrolling.scroll_stop_hard()
    actions.user.parrot_config_set_mode("default")

is_left_click_held = False

def click(button = 0, hold = False):
    global is_left_click_held
    if not (tracking.full_tracking and tracking.is_tracking):
        stopper()

    if is_left_click_held:
        ctrl.mouse_click(button=button, up=True)
        cursor.hide_border()
        is_left_click_held = False
        return
    elif hold:
        ctrl.mouse_click(button=button, down=True)
        cursor.show_border()
        is_left_click_held = True
    else:
        ctrl.mouse_click(button=button, hold=16000)
        cursor.hide_border()

def click_exit():
    click()
    actions.user.parrot_mode_v6_toggle()

def scroll(dir: str):
    tracking.freeze()
    movement.stop()
    cursor.color(RED)
    scrolling.scroll_start(dir)

def move(dir: str):
    tracking.freeze()
    scrolling.scroll_stop_hard()
    cursor.color(YELLOW)
    movement.move(dir)
    actions.user.parrot_config_set_mode("move")

def tracking_activate():
    movement.stop()
    color = TEAL if tracking.full_tracking else GREEN
    cursor.color(color)
    tracking.activate()

def tracking_toggle():
    tracking.toggle_full_tracking()
    color = TEAL if tracking.full_tracking else GREEN
    cursor.color(color)

def set_position(pos: str):
    cursor.color(RED)
    getattr(position, pos)()

def repeater():
    pass

parrot_config_pos = {
    "tut ah":       ("pos left", lambda: set_position("left")),
    "tut oh":       ("pos right", lambda: set_position("right")),
    "tut ee":       ("pos main", lambda: set_position("main")),
    "tut guh":      ("pos down", lambda: set_position("down")),
    "tut t":        ("pos up", lambda: set_position("up")),
    "tut pop":      ("pos mark", lambda: None),
    "tut eh":       ("toggle full tracking", tracking_toggle),
    "tut mm":       ("hold click", lambda: click(hold=True)),
}

parrot_config_window = {
    "er ah":        ("win left", lambda: actions.user.snap_window_to_position("left")),
    "er oh":        ("win right", lambda: actions.user.snap_window_to_position("right")),
    "er t":         ("win max", lambda: actions.user.snap_window_to_position("full")),
    "er ee":        ("win center", lambda: actions.user.snap_window_to_position("center")),
}

parrot_config_basics = {
    "eh":           ("teleport or track", tracking_activate),
    "ah":           ("move left", lambda: move("left")),
    "oh":           ("move right", lambda: move("right")),
    "guh":          ("move down", lambda: move("down")),
    "t":            ("move up", lambda: move("up")),
    "ee":           ("stop", stopper),
    "pop":          ("click exit", click_exit),
    "mm":           ("click", click),
    "hiss":         ("scroll down", lambda: scroll("down")),
    "hiss_stop":    ("", scrolling.scroll_stop_soft),
    "shush":        ("scroll up", lambda: scroll("up")),
    "shush_stop":   ("", scrolling.scroll_stop_soft),
    "palate":       ("repeater", repeater),
    "cluck":        ("exit", actions.user.parrot_mode_v6_disable),
}

parrot_config_move = {
    "shush":        ("boost large", movement.boost_large),
    "shush_stop":   ("", lambda: None),
    "hiss":         ("boost small", movement.boost_small),
    "hiss_stop":    ("", lambda: None),
    "tut":          ("slower", movement.slower),
}

parrot_config = {
    "default": {
        **parrot_config_basics,
        **parrot_config_pos,
        **parrot_config_window,
    },
    "move": {
        **parrot_config_basics,
        **parrot_config_move,
    }
}

@ctx.action_class("user")
class Actions:
    def parrot_config():
        return parrot_config

@mod.action_class
class Actions:
    def parrot_mode_v6_enable(parrot_mode: str = None):
        """Enable parrot mode"""
        global parrot_mode_enabled
        print("parrot_mode_v6_enable")
        actions.mode.disable("command")
        actions.mode.enable("user.parrot_v6")
        cursor.show(RED)
        parrot_mode_enabled = True

    def parrot_mode_v6_disable():
        """Disable parrot mode"""
        global parrot_mode_enabled
        print("parrot_mode_v6_disable")
        stopper()
        cursor.hide()
        actions.mode.disable("user.parrot_v6")
        actions.mode.enable("command")
        parrot_mode_enabled = False

    def parrot_mode_v6_toggle():
        """Toggle parrot mode"""
        if parrot_mode_enabled:
            actions.user.parrot_mode_v6_disable()
        else:
            actions.user.parrot_mode_v6_enable()