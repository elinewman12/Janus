# This object represents each note in the song, and stores data about each note
class Note:

    # Constructor, takes all fields as inputs
    def __init__(self, pitch, time, duration, velocity):
        self.pitch = pitch
        self.time = time
        self.duration = duration
        self.velocity = velocity
