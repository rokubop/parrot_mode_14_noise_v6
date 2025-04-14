from talon import actions, ctrl, cron
from .src.scrolling import scrolling
from .src.tracking import tracking
from .src.movement import movement
from .src.cursor import cursor
from .src.position import position
from .src.keys import keys
from .src.phrase import phrase

RED = "FF0000"
GREEN = "00FF00"
YELLOW = "FFFF00"
GREEN = "43e658"
TEAL = "34d5eb"

class ParrotActions:
    revive_tracking_job = None
    _is_left_click_held = False
    _parrot_mode_enabled = False

    def boost_large(self):
        """Boost the cursor movement speed briefly a large amount"""
        movement.boost_large()

    def boost_small(self):
        """Boost the cursor movement speed briefly a small amount"""
        movement.boost_small()

    def click_exit(self):
        self.click()
        self.parrot_mode_disable()

    def click_await_one_phrase(self):
        self.click()
        self.await_one_phrase()

    def await_one_phrase(self):
        self.parrot_mode_disable()
        phrase.await_next_phrase(self.parrot_mode_enable)

    def click_release(self, button = 0):
        ctrl.mouse_click(button=button, up=True)
        cursor.hide_border()
        self._is_left_click_held = False

    def click(self, button = 0, hold = False):
        position.mouse_pos_save()
        should_stop = hold != True and \
            ((not tracking.full_tracking and tracking.is_tracking) \
            or movement.is_moving() or scrolling.is_scrolling())

        if self._is_left_click_held:
            self.click_release(button)
        elif hold:
            ctrl.mouse_click(button=button, down=True)
            cursor.show_border()
            self._is_left_click_held = True
        else:
            ctrl.mouse_click(button=button, hold=16000)
            cursor.hide_border()

        if should_stop:
            self.stopper()
            if tracking.full_tracking:
                self.await_revive_tracking()

    def stop_revive_tracking(self):
        if self.revive_tracking_job:
            cron.cancel(self.revive_tracking_job)
            self.revive_tracking_job = None

    def await_revive_tracking(self):
        self.stop_revive_tracking()
        self.revive_tracking_job = cron.after("300ms", tracking.activate)

    def disable_modifiers(self):
        keys.clear_modifiers()
        cursor.clear_modifiers()

    def is_active(self):
        return tracking.is_tracking or movement.is_moving() or scrolling.is_scrolling()

    def move_or_slow(self, dir: str):
        if movement.is_moving() and actions.user.mouse_move_info().last_cardinal_dir == dir:
            movement.slower()
        else:
            self.move(dir)

    def move_slower(self):
        movement.slower()

    def move(self, dir: str):
        tracking.freeze()
        scrolling.scroll_stop_hard()
        cursor.color(YELLOW)
        movement.move(dir)
        actions.user.parrot_config_set_mode("move")

    def repeater(self):
        actions.core.repeat_phrase()

    def scroll_stop_soft(self):
        scrolling.scroll_stop_soft()

    def scroll(self, dir: str):
        tracking.freeze()
        movement.stop()
        cursor.color(RED)
        scrolling.scroll_start(dir)
        if tracking.full_tracking:
            self.stop_revive_tracking()

    def set_position(self, pos: str):
        cursor.color(RED)
        getattr(position, pos)()

    def mouse_position_restore(self):
        self.stopper()
        position.mouse_pos_cycle()

    def stopper(self):
        cursor.color(RED)
        was_active = self.is_active()
        movement.stop()
        tracking.freeze()
        scrolling.scroll_stop_hard()
        self.stop_revive_tracking()

        if not was_active:
            if self._is_left_click_held:
                self.click_release()
            keys.clear_modifiers()
            cursor.clear_modifiers()

        actions.user.parrot_config_set_mode("default")

    def toggle_modifier(self, modifier: str):
        new_state = keys.toggle_modifier(modifier)
        cursor.set_modifier(modifier, new_state)

    def tracking_activate(self):
        movement.stop()
        color = TEAL if tracking.full_tracking else GREEN
        cursor.color(color)
        tracking.activate()

    def tracking_toggle(self):
        tracking.toggle_full_tracking()
        color = TEAL if tracking.full_tracking else GREEN
        cursor.color(color)

    def parrot_mode_disable(self):
        print("parrot_mode_v6_disable")
        self.stopper()
        if self._is_left_click_held:
            self.click_release()
        keys.clear_modifiers()
        cursor.clear_modifiers()
        cursor.hide()
        scrolling.clear_scroll_stop_soft_callbacks()
        self.stop_revive_tracking()
        phrase.stop_listening()
        actions.mode.disable("user.parrot_v6")
        actions.mode.enable("command")
        self._parrot_mode_enabled = False

    def parrot_mode_enable(self):
        print("parrot_mode_v6_enable")
        actions.mode.disable("command")
        actions.mode.enable("user.parrot_v6")
        if tracking.full_tracking:
            self.tracking_activate()
            scrolling.register_scroll_stop_soft_callback(self.await_revive_tracking)
        else:
            cursor.show(RED)
        self._parrot_mode_enabled = True

    def parrot_mode_toggle(self):
        if self._parrot_mode_enabled:
            self.parrot_mode_disable()
        else:
            self.parrot_mode_enable()

parrot_actions = ParrotActions()