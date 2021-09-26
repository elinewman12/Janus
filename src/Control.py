# Stores data about tempo changes, control changes, and program changes in a song
class Control:

    def __init__(self, msg_type=None, tempo=None, control=None, value=None, instrument=None, time=None):
        self.msg_type = msg_type
        self.tempo = tempo
        self.control = control
        self.value = value
        self.instrument = instrument
        self.time = time
