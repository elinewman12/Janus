# This object represents each note in the song, and stores data about each note
NUM_NOTES = 12


class Note:

    # Constructor, takes all fields as inputs
    def __init__(self, pitch=60, time=0, duration=1, velocity=127):
        # The absolute pitch of the note
        self.pitch = pitch
        # The absolute time the note starts playing
        self.time = time
        # The duration the note is held
        self.duration = duration
        # The intensity of the note
        self.velocity = velocity
        # The pitch class the note belongs to, stored as an int from 0-11, with
        # 0 being C. Octave information is lost in this calculation.
        self.c_indexed_pitch_class = pitch % 12


