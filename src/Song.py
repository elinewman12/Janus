import Track


# Stores metadata about a song, and the tracks included in the song
class Song:
    # A list of tracks in the song
    tracks = []
    # The speed of the song (BPM? Some other format? What happens when tempo changes?
    # might need to be an array or something)
    speed = 0
    # add other fields

    # Constructor, takes a list of tracks as input
    def __init__(self, t):
        self.tracks = t
