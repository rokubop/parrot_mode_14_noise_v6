from talon import actions, cron, Module

mod = Module()

two_way_opposites = [
    ("north", "south"),
    ("upper", "downer"),
    ("up", "down"),
    ("left", "right"),
    ("push", "tug"),
    ("drain", "step"),
    ("undo", "redo"),
    ("last", "next"),
    ("forward", "back"),
    ("out", "in"),
    ("close", "reopen"),
]

opposites = {}

for key, value in two_way_opposites:
    opposites[key] = value
    opposites[value] = key

last_tut = ""
last_palate = ""

class StateReverse:
    def __init__(self):
        self.is_reverse_active = False
        self.timer_handle = None

    def activate_reverse(self):
        self.is_reverse_active = True
        if self.timer_handle:
            cron.cancel(self.timer_handle)
        self.timer_handle = cron.after("2s", self.deactivate_reverse)

    def deactivate_reverse(self):
        self.is_reverse_active = False
        self.timer_handle = None

    def is_active(self):
        return self.is_reverse_active

stateReverse = StateReverse()

def repeat():
    """Repeat the last command"""
    global last_palate, last_tut, palate_mode

    if (actions.speech.enabled()):
        if (stateReverse.is_active() and last_tut):
            last_command = actions.user.history_get(0)
            for word in opposites:
                if word in last_command:
                    if last_palate and last_palate in last_command:
                        actions.mimic(last_command)
                        last_tut = ""
                    else:
                        oppositePhrase = last_command.replace(word, opposites[word])
                        last_palate = oppositePhrase
                        actions.mimic(oppositePhrase)
                        last_tut = ""
                    return
            last_palate = ""
        else:
            actions.core.repeat_command()

        stateReverse.activate_reverse()

def reverse():
    """Reverse the last command"""
    global last_tut, last_palate

    if (actions.speech.enabled() and stateReverse.is_active()):
        last_command = actions.user.history_get(0)
        stateReverse.activate_reverse()
        for word in opposites:
            if word in last_command:
                if last_tut and last_tut in last_command:
                    actions.mimic(last_command)
                    last_palate = ""
                else:
                    oppositePhrase = last_command.replace(word, opposites[word])
                    last_tut = oppositePhrase
                    actions.mimic(oppositePhrase)
                    last_palate = ""
                return
        last_tut = ""

@mod.action_class
class Actions:
    def parrot_mode_v6_repeater():
        """Repeat last command"""
        repeat()

    def parrot_mode_v6_reverser():
        """Reverse last command"""
        reverse()
