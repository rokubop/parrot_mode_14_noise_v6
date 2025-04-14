from talon import speech_system

class Phrase:
    stop_listening_callback = None

    def on_phrase(self, p: dict):
        if p.get("text"):
            self.stop_listening()
            if self.stop_listening_callback:
                self.stop_listening_callback()
                self.stop_listening_callback = None

    def stop_listening(self):
        speech_system.unregister("post:phrase", self.on_phrase)

    def start_listening(self):
        speech_system.register("post:phrase", self.on_phrase)

    def await_next_phrase(self, callback):
        if self.stop_listening_callback:
            self.stop_listening()
        self.stop_listening_callback = callback
        self.start_listening()

phrase = Phrase()