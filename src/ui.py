from talon import Module, Context, actions, ui, skia, cron, ctrl
from talon.screen import Screen
from talon.canvas import Canvas, MouseEvent
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.skia import RoundRect
from talon.types import Rect, Point2d

canvas_cursor = None
canvas_cursor_job = None
cursor_color = "FF0000"
modifiers = set()

def on_cursor_update(c: SkiaCanvas):
    c.paint.color = cursor_color
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
        self._color = "FF0000"
        self._canvas = None
        self._update_job = None

    def on_update(self, c: SkiaCanvas):
        c.paint.color = self._color
        c.paint.style = c.paint.Style.FILL
        c.paint.textsize = 15
        (x, y) = ctrl.mouse_pos()
        c.draw_circle(x + 20, y + 20, 7)

    def freeze(self):
        if self._canvas:
            self._canvas.freeze()

    def color(self, color: str):
        self._color = color
        self.freeze()

    def show(self, color: str):
        if not self._canvas:
            current_screen = actions.user.ui_get_current_screen()
            self._canvas = Canvas.from_screen(current_screen)
            self._canvas.register("draw", self.on_update)
            self._update_job = cron.interval("16ms", self.freeze)
        self._color = color or "FF0000"
        self.freeze()

    def hide(self):
        if self._canvas:
            self._canvas.unregister("draw", self.on_update)
            cron.cancel(self._update_job)
            self._canvas.close()
            self._canvas = None
            self._update_job = None

cursor = Cursor()