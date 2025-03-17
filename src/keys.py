from talon import actions

class Keys:
    def __init__(self):
        self.modifiers = set()

    def toggle_modifier(self, key: str):
        if key in self.modifiers:
            self.modifiers.remove(key)
            actions.key(f"{key}:up")
        else:
            self.modifiers.add(key)
            actions.key(f"{key}:down")

        return key in self.modifiers

    def clear_modifiers(self):
        for key in self.modifiers:
            actions.key(f"{key}:up")
        self.modifiers.clear()

keys = Keys()