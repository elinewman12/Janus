# This object represents each note in the song, and stores data about each note
NUM_NOTES = 12

class Note:

    # Constructor, takes all fields as inputs
    def __init__(self, pitch=60, time=0, duration=1, velocity=127):
        self.pitch = pitch
        self.time = time
        self.duration = duration
        self.velocity = velocity
        self.c_indexed_pitch_class = pitch % 12
