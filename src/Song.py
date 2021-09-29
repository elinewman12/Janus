from Track import Track
from Key import Key, KEYS
from Scale import SCALE_TYPES
from Note import NUM_NOTES
import FileIO
import matplotlib.pyplot as plt
import collections

DEFAULT_TICKS_PER_BEAT = 48


# Stores metadata about a song, and the tracks included in the song
# <jmleeder>
class Song:

    def __init__(self, tracks=None, ticks_per_beat=DEFAULT_TICKS_PER_BEAT):
        if tracks is None:
            tracks = []
        self.tracks = tracks
        if ticks_per_beat >= 0:
            self.ticks_per_beat = ticks_per_beat
        else:
            raise ValueError

    # Adds a new track to the song
    def add_track(self, t):
        assert isinstance(t, Track)
        self.tracks.append(t)

    @staticmethod
    def get_notes_array():
        return KEYS

    # Saves a song object to a midi file with the given name
    #
    # <jmleeder>
    def save(self, filename, print_file=False):
        FileIO.write_midi_file(self, filename=filename, print_file=print_file)

    # Loads a file into the song object this method was called from
    # The new data overwrites any previous data stored in this song
    #
    # <jmleeder>
    def load(self, filename, print_file=False):
        FileIO.read_midi_file(self, filename=filename, print_file=print_file)

    # Deletes all of the data from a song object and resets it to default values
    #
    # <jmleeder>
    def clear_song_data(self):
        self.tracks = []
        self.ticks_per_beat = 0

    def get_c_indexed_note_frequencies(self):
        c_indexed_note_frequency = [0] * 12
        for track in self.tracks:
            if not track.is_percussion:
                track_frequencies = track.get_c_indexed_note_frequencies()
                for idx, val in enumerate(track_frequencies):
                    c_indexed_note_frequency[idx] += val
        return c_indexed_note_frequency

    def get_note_frequencies(self, key):
        indexed_note_frequency = [0] * 12
        for track in self.tracks:
            if not track.is_percussion:
                track_frequencies = track.get_note_frequencies(key)
                for idx, val in enumerate(track_frequencies):
                    indexed_note_frequency[idx] += val
            return indexed_note_frequency

    # This method will shift all notes in the song up (positive numHalfSteps) or
    # down (negative numHalfSteps) the number of half steps specified.
    # (assuming there are no key changes)
    #
    # <jfwiddif>
    def change_song_key_by_half_steps(self, num_half_steps):
        for track in self.tracks:
            if not track.is_percussion:
                for note in track.notes:
                    note.pitch += num_half_steps
        return self

    # This method will change the key of an entire song from an origin key to a destination key
    # (assuming there are no key changes)
    #
    # <jfwiddif>
    def change_song_key(self, origin_key, destination_key):

        # Check to make sure params are the correct type
        if not isinstance(origin_key, Key) or not isinstance(destination_key, Key):
            raise SyntaxError("Parameters are not of the right type.  They must be of type 'Key'")

        # Get the index of the origin key
        origin_index = origin_key.get_c_based_index_of_key()

        # Get the index of the destination key
        destination_index = destination_key.get_c_based_index_of_key()

        # discover offset (this is the number of half steps to move each note to get to the destination key)
        offset = destination_index - origin_index

        # apply the offset to each note
        for track in self.tracks:
            if not track.is_percussion:
                for note in track.notes:
                    note.pitch += offset

        return self

    # This method will change the key of a section of a song from an origin key to a destination key
    # between the provided time intervals.  Time intervals are given in absolute
    #
    #
    # <jfwiddif>
    def change_key_for_interval(self, origin_key, destination_key, interval_begin, interval_end):

        # Check to make sure params are the correct type
        if not isinstance(origin_key, Key) or not isinstance(destination_key, Key):
            raise SyntaxError("Parameters are not of the right type.  They must be of type 'Key'")

        # Get the index of the origin key
        origin_index = origin_key.get_c_based_index_of_key()

        # Get the index of the destination key
        destination_index = destination_key.get_c_based_index_of_key()

        # discover offset (this is the number of half steps to move each note to get to the destination key)
        offset = destination_index - origin_index

        # apply the offset to each note within the time interval
        for track in self.tracks:
            if not track.is_percussion:
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
        plt.show()

    # Shows a graph of the frequency of all the notes in this song
    def get_note_frequency_graph(self):
        all_notes = []
        for track in self.tracks:
            for note in track.notes:
                all_notes.append(KEYS[note.pitch % 12])

        counter = collections.Counter(all_notes)
        counter = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
        plt.bar(x=counter.keys(), height=counter.values())
        plt.xlabel("Note")
        plt.ylabel("Frequency")
        # Change this to show title of song when that variable is available
        plt.title("Frequency of Notes")
        plt.show()

    # Prints song object to the console for debugging
    #
    # <jmleeder>
    def print_song(self):
        print("Ticks per beat: " + str(self.ticks_per_beat))
        for t in self.tracks:
            print("  Track name: " + str(t.track_name))
            print("  Device name: " + str(t.device_name))
            for n in t.notes:
                print("  Pitch:" + str(n.pitch) + " Velocity: " + str(n.velocity) + " Time: " + str(n.time) +
                      " Duration: " + str(n.duration))
            for c in t.controls:
                print("  Type: " + str(c.msg_type) + " Tempo: " + str(c.tempo) + " Control: " + str(c.control) +
                      " Value: " + str(c.value) + " Instrument: " + str(c.instrument) + " Time: " + str(c.time))

    def equals(self, song):
        """ Compares if two song contain identical contents

        :param song: The song to compare to
        :return: True, if the two songs contain identical contents
        """

        if self.ticks_per_beat != song.ticks_per_beat:
            print("These songs have different ticks_per_beat values")
            print("This: " + str(self.ticks_per_beat) + ", compare to: " + str(song.ticks_per_beat))
            return False

        if len(self.tracks) != len(song.tracks):
            print("These songs have a different number of tracks")
            print("This: " + str(len(self.tracks)) + ", compare to: " + str(len(song.tracks)))
            return False

        for i, track in enumerate(self.tracks):
            if track.channel != song.tracks[i].channel:
                print("tracks " + str(i) + " have different channel values")
                print("This: " + track.channel + ", compare to: " + song.tracks[i].channel)
                return False

            if track.track_name != song.tracks[i].track_name:
                print("tracks " + str(i) + " have different track names :")
                print("This: '" + track.track_name + "', compare to: '" + song.tracks[i].track_name + "'")
                return False

            if track.device_name != song.tracks[i].device_name:
                print("tracks " + str(i) + " have different device names")
                print("This: '" + track.device_name + "', compare to: '" + song.tracks[i].device_name + "'")
                return False

            if len(track.controls) != len(song.tracks[i].controls):
                print("tracks " + str(i) + " have different numbers of control messages")
                print("This: " + str(len(track.controls)) + ", compare to: " + str(len(song.tracks[i].controls)))
                return False

            for j, control in enumerate(track.controls):
                if control.msg_type != song.tracks[i].controls[j].msg_type:
                    print("tracks " + str(i) + " control " + str(j) + " have different message types")
                    print("This: '" + control.msg_type + "', compare to: '" + song.tracks[i].controls[j].msg_type + "'")
                    return False

                if control.control != song.tracks[i].controls[j].control:
                    print("tracks " + str(i) + " control " + str(j) + " have different control numbers")
                    print("This: " + str(control.control) + ", compare to: " + str(song.tracks[i].controls[j].control))
                    return False

                if control.value != song.tracks[i].controls[j].value:
                    print("tracks " + str(i) + " control " + str(j) + " have different values")
                    print("This: " + str(control.value) + ", compare to: " + str(song.tracks[i].controls[j].value))
                    return False

                if control.tempo != song.tracks[i].controls[j].tempo:
                    print("tracks " + str(i) + " control " + str(j) + " have different tempos")
                    print("This: " + str(control.tempo) + ", compare to: " + str(song.tracks[i].controls[j].tempo))
                    return False

                if control.instrument != song.tracks[i].controls[j].instrument:
                    print("tracks " + str(i) + " control " + str(j) + " have different instruments")
                    print("This: " + str(control.instrument) + ", compare to: " + str(
                        song.tracks[i].controls[j].instrument))
                    return False

                if control.time != song.tracks[i].controls[j].time:
                    print("tracks " + str(i) + " control " + str(j) + " have different times")
                    print("This: " + str(control.time) + ", compare to: " + str(song.tracks[i].controls[j].time))
                    return False

            if len(track.notes) != len(song.tracks[i].notes):
                print("tracks " + str(i) + " have different numbers of notes")
                print("This: " + str(len(track.notes)) + ", compare to: " + str(len(song.tracks[i].notes)))
                return False

            for j, note in enumerate(track.notes):
                if note.pitch != song.tracks[i].notes[j].pitch:
                    print("tracks " + str(i) + " note " + str(j) + " have different pitches")
                    print("This: " + str(note.pitch) + ", compare to: " + str(song.tracks[i].notes[j].pitch))
                    return False

                if note.time != song.tracks[i].notes[j].time:
                    print("tracks " + str(i) + " note " + str(j) + " have different times")
                    print("This: " + str(note.time) + ", compare to: " + str(song.tracks[i].notes[j].time))
                    return False

                if note.duration != song.tracks[i].notes[j].duration:
                    print("tracks " + str(i) + " note " + str(j) + " have different durations")
                    print("This: " + str(note.duration) + ", compare to: " + str(song.tracks[i].notes[j].duration))
                    return False

                if note.velocity != song.tracks[i].notes[j].velocity:
                    print("tracks " + str(i) + " note " + str(j) + " have different velocities")
                    print("This: " + str(note.velocity) + ", compare to: " + str(song.tracks[i].notes[j].velocity))
                    return False

        return True

    def detect_key(self):
        note_frequencies = self.get_c_indexed_note_frequencies()

        key_and_scale_error_record = {}

        # Iterate over each key
        for key in KEYS:
            # we have to rotate the frequency array to be 0 indexed at the key.
            # get the index of the key we want the frequencies indexed by
            key_index = Key(key).get_c_based_index_of_key()

            # rotate the array left based on the index to have the 0th index contain the frequency of the tonic or key
            key_indexed_note_frequencies = note_frequencies[key_index:] + note_frequencies[:key_index]

            # iterate over each scale and count errors for each
            for scale in SCALE_TYPES.items():

                # Break the scale dict into key and value
                scale_name = scale[0]
                scale_steps = scale[1]

                # keep an error counter to increment each time a note is not in the key/scale
                errors = 0

                # generate an array with true in the indexes that are in the key/scale and false in the
                # indexes that are notes that are out of the scale  (the array is key indexed at 0)
                accepted_notes = [False] * NUM_NOTES

                # semitones that a note in the scale is away from the key (starts at 0 because regardless of scale the
                # tonic will be in the scale)
                semitones_from_key = 0
                accepted_notes[0] = True

                # iterate through the scale semitones marking notes as valid for the key/scale
                for semitones in scale_steps:
                    semitones_from_key += semitones
                    # % number of notes (12) because some signatures will count semitones back to tonic
                    accepted_notes[semitones_from_key % NUM_NOTES] = True

                # count all of the errors that occur (notes in the song that are not accepted by key/scale)
                for idx in range(NUM_NOTES):
                    if accepted_notes[idx]:
                        continue
                    else:
                        errors += key_indexed_note_frequencies[idx]

                # store errors in a record dictionary
                key_and_scale_error_record[key + ' ' + scale_name] = errors

        # find the key/scales with the minimum values in the error dictionary
        minimum_errors = min(key_and_scale_error_record.values())
        result = [k for k, v in key_and_scale_error_record.items() if v == minimum_errors]

        return result
