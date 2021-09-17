from matplotlib import pyplot

from Track import Track
import FileIO
import matplotlib.pyplot as plt
import collections

NOTES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
EQUIVALENCE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


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

    def get_c_indexed_note_frequencies(self):
        c_indexed_note_frequency = [0] * 12
        for track in self.tracks:
            track_frequencies = track.get_c_indexed_note_frequencies()
            for idx, val in enumerate(track_frequencies):
                c_indexed_note_frequency[idx] += val
        return c_indexed_note_frequency

    # This method will shift all notes in the song up (positive numHalfSteps) or
    # down (negative numHalfSteps) the number of half steps specified.
    # (assuming there are no key changes)
    #
    # <jfwiddif>
    def change_song_key_by_half_steps(self, num_half_steps):
        for track in self.tracks:
            for note in track.notes:
                note.pitch += num_half_steps
        return self

    # This method will change the key of an entire song from an origin key to a destination key
    # (assuming there are no key changes)
    #
    # <jfwiddif>
    def change_song_key(self, origin_key, destination_key):
        origin_index = 0
        destination_index = 0
        offset = 0

        # Get the index of the origin key
        if origin_key in NOTES:
            origin_index = NOTES.index(origin_key)
        elif origin_key in EQUIVALENCE:
            origin_index = EQUIVALENCE.index(origin_key)
        else:
            raise SyntaxError("Origin Key needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")

        # Get the index of the destination key
        if destination_key in NOTES:
            destination_index = NOTES.index(destination_key)
        elif destination_key in EQUIVALENCE:
            destination_index = EQUIVALENCE.index(destination_key)
        else:
            raise SyntaxError("Destination Key needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")

        # discover offset (this is the number of half steps to move each note to get to the destination key)
        offset = destination_index - origin_index

        # apply the offset to each note
        for track in self.tracks:
            for note in track.notes:
                note.pitch += offset

        return self

    # This method will change the key of a section of a song from an origin key to a destination key
    # between the provided time intervals.  Time intervals are given in absolute
    #
    #
    # <jfwiddif>
    def change_key_for_interval(self, origin_key, destination_key, interval_begin, interval_end):
        origin_index = 0
        destination_index = 0
        offset = 0

        # Get the index of the origin key
        if origin_key in NOTES:
            origin_index = NOTES.index(origin_key)
        elif origin_key in EQUIVALENCE:
            origin_index = EQUIVALENCE.index(origin_key)
        else:
            raise SyntaxError("Origin Key needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")

        # Get the index of the destination key
        if destination_key in NOTES:
            destination_index = NOTES.index(destination_key)
        elif destination_key in EQUIVALENCE:
            destination_index = EQUIVALENCE.index(destination_key)
        else:
            raise SyntaxError("Destination Key needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")

        # discover offset (this is the number of half steps to move each note to get to the destination key)
        offset = destination_index - origin_index

        # apply the offset to each note within the time interval
        for track in self.tracks:
            for note in track.notes:
                if interval_begin <= note.time <= interval_end:
                    note.pitch += offset
        return self

    # Shows a graph of the velocity of all the notes in this song
    def get_note_velocity_graph(self):
        all_velocity = []
        all_time = []
        for track in self.tracks:
            for note in track.notes:
                all_velocity.append(note.velocity)
                all_time.append(note.time)

        plt.plot(all_time, all_velocity)
        plt.xlabel("Time")
        plt.ylabel("Velocity")
        # Change this to show title of song when that variable is available
        plt.title("Velocity of Notes")
        pyplot.show()

    # Shows a graph of the frequency of all the notes in this song
    def get_note_frequency_graph(self):
        all_notes = []
        for track in self.tracks:
            for note in track.notes:
                all_notes.append(NOTES[note.pitch % 12])

        counter = collections.Counter(all_notes)
        counter = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
        plt.bar(x=counter.keys(), height=counter.values())
        plt.xlabel("Note")
        plt.ylabel("Frequency")
        # Change this to show title of song when that variable is available
        plt.title("Frequency of Notes")
        plt.show()
