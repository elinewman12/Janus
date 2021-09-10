from Track import Track
import FileIO


# Stores metadata about a song, and the tracks included in the song
# <jmleeder>
class Song:

    def __init__(self, tracks=None, ticks_per_beat=0):
        if tracks is None:
            tracks = []
        self.tracks = tracks
        self.ticks_per_beat = ticks_per_beat

    def add_track(self, t):
        assert isinstance(t, Track)
        self.tracks.append(t)

    # Saves a song object to a midi file with the given name
    #
    # <jmleeder>
    def save(self, filename):
        FileIO.write_midi_file(self, filename)

    # Loads a file into the song object this method was called from
    # The new data overwrites any previous data stored in this song
    #
    # <jmleeder>
    def load(self, filename):
        FileIO.read_midi_file(self, filename)

    # Deletes all of the data from a song object and resets it to default values
    #
    # <jmleeder>
    def clear_song_data(self):
        self.tracks = []
        self.ticks_per_beat = 0
