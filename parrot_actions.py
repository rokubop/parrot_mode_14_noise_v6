from talon import actions, ctrl
from .src.scrolling import scrolling
from .src.tracking import tracking
from .src.movement import movement
from .src.cursor import cursor
from .src.position import position
from .src.keys import keys

RED = "FF0000"
GREEN = "00FF00"
YELLOW = "FFFF00"
GREEN = "43e658"
TEAL = "34d5eb"

class ParrotActions:
    def __init__(self):
        self._is_left_click_held = False
        self._parrot_mode_enabled = False

    def is_active(self):
        return tracking.is_tracking or movement.is_moving() or scrolling.is_scrolling()

    def boost_large(self):
        """Boost the cursor movement speed briefly a large amount"""
        movement.boost_large()

    def boost_small(self):
        """Boost the cursor movement speed briefly a small amount"""
        movement.boost_small()

    def move_slower(self):
        movement.slower()

    def scroll_stop_soft(self):
        scrolling.scroll_stop_soft()

    def stopper(self):
        cursor.color(RED)
        was_active = self.is_active()
        movement.stop()
        tracking.freeze()
        scrolling.scroll_stop_hard()

        if not was_active:
            # and mouse too!
            keys.clear_modifiers()
            cursor.clear_modifiers()

        actions.user.parrot_config_set_mode("default")

    def click(self, button = 0, hold = False):
        should_stop = hold == False and not (tracking.full_tracking and tracking.is_tracking)

        if self._is_left_click_held:
            ctrl.mouse_click(button=button, up=True)
            cursor.hide_border()
            self._is_left_click_held = False
            return
        elif hold:
            ctrl.mouse_click(button=button, down=True)
            cursor.show_border()
            self._is_left_click_held = True
        else:
            ctrl.mouse_click(button=button, hold=16000)
            cursor.hide_border()

        if should_stop:
            self.stopper()

    def click_exit(self):
        self.click()
        self.parrot_mode_disable()

    def scroll(self, dir: str):
        tracking.freeze()
        movement.stop()
        cursor.color(RED)
        scrolling.scroll_start(dir)

    def move(self, dir: str):
        tracking.freeze()
        scrolling.scroll_stop_hard()
        cursor.color(YELLOW)
        movement.move(dir)
        actions.user.parrot_config_set_mode("move")

    def tracking_activate(self):
        movement.stop()
        color = TEAL if tracking.full_tracking else GREEN
        cursor.color(color)
        tracking.activate()

    def tracking_toggle(self):
        tracking.toggle_full_tracking()
        color = TEAL if tracking.full_tracking else GREEN
        cursor.color(color)

    def set_position(self, pos: str):
        cursor.color(RED)
        getattr(position, pos)()

    def repeater(self):
        pass

    def toggle_modifier(self, modifier: str):
        new_state = keys.toggle_modifier(modifier)
        cursor.set_modifier(modifier, new_state)

    def disable_modifiers(self):
        keys.clear_modifiers()
        cursor.clear_modifiers()

    def parrot_mode_enable(self):
        print("parrot_mode_v6_enable")
        actions.mode.disable("command")
        actions.mode.enable("user.parrot_v6")
        cursor.show(RED)
        self._parrot_mode_enabled = True

    def parrot_mode_disable(self):
        print("parrot_mode_v6_disable")
        self.stopper()
        keys.clear_modifiers()
        cursor.clear_modifiers()
        cursor.hide()
        actions.mode.disable("user.parrot_v6")
        actions.mode.enable("command")
        self._parrot_mode_enabled = False

    def parrot_mode_toggle(self):
        if self._parrot_mode_enabled:
            self.parrot_mode_disable()
        else:
            self.parrot_mode_enable()

parrot_actions = ParrotActions()