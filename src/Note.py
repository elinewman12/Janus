# This object represents each note in the song, and stores data about each note
class Note:
    # The absolute pitch of the note, as an integer
    pitch = 0
    # The absolute time this note occurs in the song
    time = 0
    # The duration of this note
    duration = 0;
    # The intensity of the note
    velocity = 0

    # Constructor, takes all fields as inputs
    def __init__(self, p, t, d, v):
        self.pitch = p
        self.time = t
        self.duration = d
        self.velocity = v
