from talon import actions

full_tracking = False
is_tracking = False

def location():
    print("location")

def click():
    stopper()
    actions.mouse_click(0)

def toggle_parrot_v6():
    actions.user.parrot_mode_v6_toggle()

def mouse_move_continuous(dir: str):
    tracking_halt()
    if dir == "left":
        actions.user.mouse_move_continuous(-1, 0)
    elif dir == "right":
        actions.user.mouse_move_continuous(1, 0)
    elif dir == "up":
        actions.user.mouse_move_continuous(0, -1)
    elif dir == "down":
        actions.user.mouse_move_continuous(0, 1)

def mouse_jump_and_move_continuous(dir: str):
    actions.tracking.jump()
    mouse_move_continuous(dir)

def mouse_move_smooth_to_gaze():
    tracking_halt()
    x = actions.mouse_x()
    y = actions.mouse_y()
    actions.tracking.jump()
    gaze_x = actions.mouse_x()
    gaze_y = actions.mouse_y()
    actions.mouse_move(x, y)
    actions.user.mouse_move_smooth_from_to(x, y, gaze_x, gaze_y)

def mouse_move_smooth_from_gaze():
    tracking_halt()
    x = actions.mouse_x()
    y = actions.mouse_y()
    actions.tracking.jump()
    gaze_x = actions.mouse_x()
    gaze_y = actions.mouse_y()
    actions.user.mouse_move_smooth_from_to(gaze_x, gaze_y, x, y)

def shove_modifier():
    tracking_halt()
    amount = 200
    info = actions.user.mouse_move_info()
    unit_vector = info["last_unit_vector"]

    def continue_slowly():
        actions.user.mouse_move_continuous(unit_vector.x, unit_vector.y)

    actions.user.mouse_move_smooth_delta(
        unit_vector.x * amount,
        unit_vector.y * amount,
        callback_stop=continue_slowly
    )

def scan_modifier():
    tracking_halt()
    actions.user.mouse_scroll_down()

def mouse_shove_and_move(dir: str):
    shove_modifier()
    mouse_move_continuous(dir)

def stopper():
    mouse_move_stop()
    tracking_halt()

def mouse_move_stop():
    actions.user.mouse_move_continuous_stop()

def jump_to_gaze_and_head_track():
    global is_tracking
    mouse_move_stop()
    if not actions.tracking.control_enabled():
        actions.tracking.control_toggle(True)
    actions.tracking.control_head_toggle(False)
    actions.tracking.control_gaze_toggle(True)
    actions.sleep("30ms")
    actions.tracking.control_gaze_toggle(False)
    actions.tracking.control_head_toggle(True)
    is_tracking = True

def tracking_halt():
    global is_tracking
    if is_tracking:
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(False)
        is_tracking = False

def toggle_full_tracking():
    global full_tracking
    if full_tracking:
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(False)
    else:
        actions.tracking.control_gaze_toggle(True)
        actions.tracking.control_head_toggle(True)
    full_tracking = not full_tracking