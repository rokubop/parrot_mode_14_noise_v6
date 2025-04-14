from talon import Module, actions, storage

class Tracking():
    FULL_TRACKING_ID = "parrot_v6.full_tracking"

    def __init__(self):
        self.is_tracking = False
        self.full_tracking = storage.get(self.FULL_TRACKING_ID, False)

    def activate(self):
        if not actions.tracking.control_enabled():
            actions.tracking.control_toggle(True)

        if self.full_tracking:
            self.full_track_enable()
        else:
            self.teleport_and_track_head()

    def full_track_enable(self):
        actions.tracking.control_gaze_toggle(True)
        actions.tracking.control_head_toggle(True)
        self.is_tracking = True
        storage.set(self.FULL_TRACKING_ID, True)

    def teleport_and_track_head(self):
        actions.tracking.control_head_toggle(False)
        actions.tracking.control_gaze_toggle(True)
        actions.sleep("50ms")
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(True)
        self.is_tracking = True

    def freeze(self):
        if self.is_tracking:
            actions.tracking.control_head_toggle(False)
            actions.tracking.control_gaze_toggle(False)
            self.is_tracking = False

    def toggle_full_tracking(self):
        if self.full_tracking:
            self.teleport_and_track_head()
            storage.set(self.FULL_TRACKING_ID, False)
        else:
            self.full_track_enable()

        self.full_tracking = not self.full_tracking


tracking = Tracking()