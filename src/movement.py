from talon import actions

class Movement():
    def move(self, direction):
        if direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()
        elif direction == "up":
            self.move_up()
        elif direction == "down":
            self.move_down()

    def move_left(self):
        actions.user.mouse_move_continuous(-1, 0)

    def move_right(self):
        actions.user.mouse_move_continuous(1, 0)

    def move_up(self):
        actions.user.mouse_move_continuous(0, -1)

    def move_down(self):
        actions.user.mouse_move_continuous(0, 1)

    def boost_large(self):
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

    def boost_small(self):
        amount = 50
        info = actions.user.mouse_move_info()
        unit_vector = info["last_unit_vector"]

        def continue_slowly():
            actions.user.mouse_move_continuous(unit_vector.x, unit_vector.y)

        actions.user.mouse_move_smooth_delta(
            unit_vector.x * amount,
            unit_vector.y * amount,
            callback_stop=continue_slowly
        )

    def slower(self):
        actions.user.mouse_move_continuous_speed_decrease()

    def stop(self):
        actions.user.mouse_move_continuous_stop()

movement = Movement()
