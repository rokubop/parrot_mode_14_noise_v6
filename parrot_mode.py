from talon import Module, Context
from .parrot_actions import parrot_actions

mod = Module()
mod.mode("parrot_v6", "parrot mode v6")

ctx_parrot_mode = Context()
ctx_parrot_mode.matches = """
mode: user.parrot_v6
"""

parrot_config_basics = {
    "eh":           ("teleport/track", parrot_actions.tracking_activate),
    "ah:th_90":     ("move left", lambda: parrot_actions.move_or_slow("left")),
    "oh:th_90":     ("move right", lambda: parrot_actions.move_or_slow("right")),
    "guh":          ("move down", lambda: parrot_actions.move_or_slow("down")),
    "t":            ("move up", lambda: parrot_actions.move_or_slow("up")),
    "ee":           ("stop", parrot_actions.stopper),
    "er":           ("last mouse pos", parrot_actions.mouse_position_restore),
    "mm":           ("click", parrot_actions.click),
    "hiss":         ("scroll down", lambda: parrot_actions.scroll("down")),
    "hiss_stop":    ("", parrot_actions.scroll_stop_soft),
    "shush":        ("scroll up", lambda: parrot_actions.scroll("up")),
    "shush_stop":   ("", parrot_actions.scroll_stop_soft),
    "palate":       ("repeater", parrot_actions.repeater),
    "pop":          ("click exit", parrot_actions.click_exit),
    "cluck":        ("exit", parrot_actions.parrot_mode_disable),
}

parrot_config_utilities = {
    "tut mm":      ("left click drag", lambda: parrot_actions.click(hold=True)),
    # "tut mm":       ("middle click drag", lambda: parrot_actions.click(button=2, hold=True)),
    "tut oh":       ("right click", lambda: parrot_actions.click(button=1)),
    "tut t":        ("toggle shift", lambda: parrot_actions.toggle_modifier("shift")),
    "tut guh":      ("toggle control", lambda: parrot_actions.toggle_modifier("ctrl")),
    "tut ah":       ("toggle alt", lambda: parrot_actions.toggle_modifier("alt")),
    "tut eh":       ("toggle full tracking", parrot_actions.tracking_toggle),
}

parrot_config_pos = {
    "er ah":       ("pos left", lambda: parrot_actions.set_position("left")),
    "er oh":       ("pos right", lambda: parrot_actions.set_position("right")),
    "er ee":       ("pos main", lambda: parrot_actions.set_position("main")),
    "er guh":      ("pos down", lambda: parrot_actions.set_position("down")),
    "er t":        ("pos up", lambda: parrot_actions.set_position("up")),
    "er pop":      ("pos mark", lambda: None),
}

parrot_config_move = {
    "shush":        ("boost large", parrot_actions.boost_large),
    "shush_stop":   ("", lambda: None),
    "hiss":         ("boost small", parrot_actions.boost_small),
    "hiss_stop":    ("", lambda: None),
}

parrot_config = {
    "default": {
        **parrot_config_basics,
        **parrot_config_utilities,
        **parrot_config_pos,
    },
    "move": {
        **parrot_config_basics,
        **parrot_config_move,
    }
}

@ctx_parrot_mode.action_class("user")
class Actions:
    def parrot_config():
        return parrot_config

@mod.action_class
class Actions:
    def parrot_mode_v6_enable():
        """Enable parrot mode"""
        parrot_actions.parrot_mode_enable()

    def parrot_mode_v6_disable():
        """Disable parrot mode"""
        parrot_actions.parrot_mode_disable()

    def parrot_mode_v6_toggle():
        """Toggle parrot mode"""
        parrot_actions.parrot_mode_toggle()