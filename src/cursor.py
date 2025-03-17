from talon import actions, cron, ctrl
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas

canvas_cursor = None
canvas_cursor_job = None
default_cursor_color = "FF0000"
default_border_color = "FFFFFF"

class Cursor:
    def __init__(self):
        self._color = default_cursor_color
        self._border_color = default_border_color
        self._border_show = False
        self._canvas = None
        self._update_job = None
        self._modifiers = set()

    def on_update(self, c: SkiaCanvas):
        (x, y) = ctrl.mouse_pos()

        # border
        if self._border_show:
            c.paint.color = "000000"
            c.paint.style = c.paint.Style.FILL
            c.draw_circle(x + 20, y + 20, 11)

            c.paint.color = self._border_color
            c.paint.style = c.paint.Style.FILL
            c.draw_circle(x + 20, y + 20, 10)

            c.paint.color = "000000"
            c.paint.style = c.paint.Style.FILL
            c.paint.textsize = 15
            c.draw_circle(x + 20, y + 20, 8)

        # main circle
        c.paint.color = self._color
        c.paint.style = c.paint.Style.FILL
        c.paint.textsize = 15
        c.draw_circle(x + 20, y + 20, 7)

        # modifier circles (shift, ctrl, alt)
        offset_x = 31
        offset_increment = 11
        if "shift" in self._modifiers:
            c.paint.color = "0490c9"
            c.draw_circle(x + offset_x, y + 30, 5)
            offset_x += offset_increment

        if "ctrl" in self._modifiers:
            c.paint.color = "84E773"
            c.draw_circle(x + offset_x, y + 30, 5)
            offset_x += offset_increment

        if "alt" in self._modifiers:
            c.paint.color = "FF6DD9"
            c.draw_circle(x + offset_x, y + 30, 5)

    def freeze(self):
        if self._canvas:
            self._canvas.freeze()

    def color(self, color: str):
        self._color = color
        self.freeze()

    def show_border(self):
        if not self._border_show:
            self._border_show = True
            self.freeze()

    def hide_border(self):
        if self._border_show:
            self._border_show = False
            self.freeze()

    def add_modifier(self, modifier: str):
        """e.g. shift, ctrl, alt"""
        self._modifiers.add(modifier)
        self.freeze()

    def remove_modifier(self, modifier: str):
        """e.g. shift, ctrl, alt"""
        self._modifiers.remove(modifier)
        self.freeze()

    def set_modifier(self, modifier: str, is_active: bool):
        """e.g. shift, ctrl, alt"""
        self._modifiers.add(modifier) if is_active else self._modifiers.remove(modifier)

    def clear_modifiers(self):
        self._modifiers.clear()

    def show(self, color: str):
        self._color = color or default_cursor_color
        if not self._canvas:
            current_screen = actions.user.ui_get_current_screen()
            self._canvas = Canvas.from_screen(current_screen)
            self._canvas.register("draw", self.on_update)
            self._update_job = cron.interval("16ms", self.freeze)
        self.freeze()

    def hide(self):
        self.clear_modifiers()
        if self._canvas:
            self._canvas.unregister("draw", self.on_update)
            cron.cancel(self._update_job)
            self._canvas.close()
            self._canvas = None
            self._update_job = None

cursor = Cursor()