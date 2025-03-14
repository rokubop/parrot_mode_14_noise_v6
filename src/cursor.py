from talon import actions, cron, ctrl
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas

canvas_cursor = None
canvas_cursor_job = None
default_cursor_color = "FF0000"
default_border_color = "FFFFFF"
modifiers = set()

def on_cursor_update(c: SkiaCanvas):
    c.paint.color = default_cursor_color
    c.paint.style = c.paint.Style.FILL
    c.paint.textsize = 15
    (x, y) = ctrl.mouse_pos()
    c.draw_circle(x + 20, y + 20, 7)

def freeze_canvas():
    if canvas_cursor:
        canvas_cursor.freeze()

def clear():
    global canvas_cursor, canvas_cursor_job
    if canvas_cursor:
        canvas_cursor.unregister("draw", on_cursor_update)
        cron.cancel(canvas_cursor_job)
        canvas_cursor = None
        canvas_cursor_job = None

class Cursor:
    def __init__(self):
        self._color = default_cursor_color
        self._border_color = default_border_color
        self._border_show = False
        self._canvas = None
        self._update_job = None

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

    def show(self, color: str):
        if not self._canvas:
            current_screen = actions.user.ui_get_current_screen()
            self._canvas = Canvas.from_screen(current_screen)
            self._canvas.register("draw", self.on_update)
            self._update_job = cron.interval("16ms", self.freeze)
        self._color = color or default_cursor_color
        self.freeze()

    def hide(self):
        if self._canvas:
            self._canvas.unregister("draw", self.on_update)
            cron.cancel(self._update_job)
            self._canvas.close()
            self._canvas = None
            self._update_job = None

cursor = Cursor()