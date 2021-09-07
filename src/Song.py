from Track import Track


# Stores metadata about a song, and the tracks included in the song
class Song:
    # A list of tracks in the song
    tracks = []
    # The speed of the song
    ticks_per_beat = 0
    # add other fields

    def addTrack(self, t):
        assert isinstance(t, Track)
        self.tracks.append(t)
