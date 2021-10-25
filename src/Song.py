import logging
from logging import info
from Track import Track, TagEnum
from Key import Key, KEYS
from scale import SCALE_TYPES
from Note import NUM_NOTES
import file_io as FileIO
# import matplotlib.pyplot as plt
import collections

DEFAULT_TICKS_PER_BEAT = 48


# Stores metadata about a song, and the tracks included in the song
# <jmleeder>
class Song:

    def __init__(self, tracks=None, ticks_per_beat=DEFAULT_TICKS_PER_BEAT):
        """ Constructor for the Song class.

        Args:
            tracks (Track[], optional): List of Tracks that make up the song. Defaults to None.
            ticks_per_beat (int, optional): The amount of ticks that pass within one beat in the 
                song. Defaults to DEFAULT_TICKS_PER_BEAT (48).

        Raises:
            ValueError: For a negative ticks_per_beat value
        """
        if tracks is None:
            tracks = []
        self.tracks = tracks
        if ticks_per_beat >= 0:
            self.ticks_per_beat = ticks_per_beat
        else:
            raise ValueError

    def add_track(self, t):
        """ Adds a new track to the song.

        Args:
            t (Track): Track to add to the song
        """
        assert isinstance(t, Track)
        self.tracks.append(t)

    @staticmethod
    def get_notes_array():
        """ TODO: ?

        Returns:
            String[]: List of each key possible represented as strings.
        """
        return KEYS

    def save(self, filename, print_file=False):
        """ Saves a song object to a midi file with the given name

        Args:
            filename (String): Name of file to save the song as
            print_file (bool, optional): Whether or not to print out the song. Mainly 
                used for debugging purposes. Defaults to False.
        """
        FileIO.write_midi_file(self, filename=filename, print_file=print_file)

    def load(self, filename, print_file=False):
        """ Loads a file into this song object. The new data overwrites any previous
        data stored in this song.

        Args:
            filename (String): Name of the file to load in
            print_file (bool, optional): Whether or not to print out the song. Mainly 
                used for debugging purposes. Defaults to False.
        """
        FileIO.read_midi_file(self, filename=filename, print_file=print_file)

    def clear_song_data(self):
        """ Deletes all of the data from this song object and resets its default values
        """
        self.tracks = []
        self.ticks_per_beat = DEFAULT_TICKS_PER_BEAT

    def get_c_indexed_note_frequencies(self):
        """ Returns an array containing how many times each of the 12 notes appears in this 
        song, starting with C.

        Returns:
            int[]: note frequencies array
        """
        c_indexed_note_frequency = [0] * 12
        for track in self.tracks:
            if not track.is_percussion:
                track_frequencies = track.get_c_indexed_note_frequencies()
                for idx, val in enumerate(track_frequencies):
                    c_indexed_note_frequency[idx] += val
        return c_indexed_note_frequency

    def get_note_frequencies(self, key):
        """ Returns an array containing how many times each of the 12 notes appears in this 
        song, starting with key.

        Args:
            key (Key): Key to start the array with

        Returns:
            int[]: note frequencies array
        """
        indexed_note_frequency = [0] * 12
        for track in self.tracks:
            if not track.is_percussion:
                track_frequencies = track.get_note_frequencies(key)
                for idx, val in enumerate(track_frequencies):
                    indexed_note_frequency[idx] += val
            return indexed_note_frequency

    def change_song_key_by_half_steps(self, num_half_steps):
        """ Shifts all notes in the song up the by num_half_steps half steps.
        If num_half_steps is negative, the notes will be shifted down instead
        of up.

        Args:
            num_half_steps (int): Number of half steps to move the notes in the song by

        Returns:
            Song: The newly edited song.
        """
        for track in self.tracks:
            if not track.is_percussion:
                for note in track.notes:
                    note.pitch += num_half_steps
        return self

    def change_song_key(self, origin_key, destination_key):
        """ Changes the key of an entire song from an origin key to a desintaiton key
        TODO: Will not need origin_key param once key detection is fully implemented and tested

        Args:
            origin_key (Key): current key of the song
            destination_key (Key): key to change the song to

        Raises:
            SyntaxError: If origin_key or destination_key is not a valid Key

        Returns:
            Song: The newly edited song
        """

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

    def change_key_for_interval(self, origin_key, destination_key, interval_begin, interval_end):
        """ Changes the key of a song for a certain time interval during it.
        TODO: this will not need origin_key once key detection is fully implemented

        Args:
            origin_key (Key): Current key of the song
            destination_key (Key): Key to change the song to
            interval_begin (int): Absolute time during the song to start the key change
            interval_end (int): Absolute time during the song to end the key change

        Raises:
            SyntaxError: If origin_key or destination_key is not a valid Key

        Returns:
            Song: the newly edited song
        """

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

    def get_note_velocity_graph(self, name):
        """ Shows a graph of the velocity (intensity/loudness) of all the notes in this song.
        TODO: make this return rather than 'print'
        """
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
        plt.title("Velocity of Notes in " + name)
        plt.show()

    def get_bar_graph(self, title, x_label, y_label, items):
        counter = collections.Counter(items)
        counter = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
        bar = plt.bar(x=counter.keys(), height=counter.values())
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        # Change this to show title of song when that variable is available
        plt.title(title)
        return bar

    # Shows a graph of the frequency of all the notes in this song
    def get_note_frequency_graph(self, name):
        """ Shows a graph of the frequency that each note apperas in this song.
        TODO: make this return rather than 'print'
        """
        all_notes = []
        for track in self.tracks:
            for note in track.notes:
                all_notes.append(KEYS[note.pitch % 12])

        graph = self.get_bar_graph("Frequency of Notes in " + name, "Note", "Frequency", all_notes)
        plt.show()

    def to_string(self):
        """ Returns the contents of the song as a string in the format: \n
        Song metadata       \n
        Track1 metadata     \n
        notes               \n
        ...V...             \n
        control messages    \n
        ...V...             \n
        Track 2 metadata    \n
        notes               \n
        ...V...             \n
        etc

        Note: The notes and control messages are listed separately, they are not sorted together by time.
        """
        message = ""
        message += ("Ticks per beat: " + str(self.ticks_per_beat) + "\n")
        for t in self.tracks:
            message += ("  Track name: " + str(t.track_name) + "\n")
            message += ("  Device name: " + str(t.device_name) + "\n")
            for n in t.notes:
                message += ("  Pitch:" + str(n.pitch) + " Velocity: " + str(n.velocity) + " Time: " + str(n.time) +
                            " Duration: " + str(n.duration) + " Channel: " + str(n.channel) + "\n")
            for c in t.controls:
                message += (
                        "  Type: " + str(c.msg_type) + " Tempo: " + str(c.tempo) + " Control: " + str(c.control) +
                        " Value: " + str(c.value) + " Instrument: " + str(c.instrument) + " Time: " + str(c.time) +
                        "\n")
        return message

    def equals(self, song):
        """ Determines whether this song and the specified song are equivalent.

        Args:
            song (Song): Song to check this song against

        Returns:
            bool: True if the songs are equivalent, false otherwise
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

                if note.channel != song.tracks[i].notes[j].channel:
                    print("tracks " + str(i) + " note " + str(j) + " have different channels")
                    print("This: " + str(note.channel) + ", compare to: " + str(song.tracks[i].notes[j].channel))
                    return False

        return True
     
    def detect_key_and_scale(self):
        """ Detect the key of a song using Mr. Dehaan's algorithm.  This algorithm generates the valid notes
        for every key and for every scale and checks the occurrences of the notes in the song against the valid
        key/scale notes.  It then finds how many errors (or misses) occurred.  It then finds the key/scale with the
        lowest number of errors (or the list of key/scale with the same minimum) and returns the result.

        :param display_result: determines if you receive output to console about the algorithms findings (default False)
        :return: A list containing the keys and scales that were detected.  ex -> ['C major', 'D minor']
        """
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
                    if not accepted_notes[idx]:
                        errors += key_indexed_note_frequencies[idx]

                # store errors in a record dictionary
                key_and_scale_error_record[key + ' ' + scale_name] = errors

        # find the key/scales with the minimum values in the error dictionary
        minimum_errors = min(key_and_scale_error_record.values())
        result = [k for k, v in key_and_scale_error_record.items() if v == minimum_errors]

        # now we have the relative major and minors, we can use the note frequencies to differentiate
        # between the two based on the assumption that for most cases the tonic will be played more than
        # other notes.  This lets us differentiate scales with the same notes such as D major and B Minor.

        # get the resulting keys/scales
        relative_major_key_scale = result[0]
        relative_minor_key_scale = result[1]

        # Create the key object to hold potential tonic
        (key, scale) = relative_major_key_scale.split()
        relative_major_key = Key(tonic=key, mode=scale)
        relative_minor_key = Key(tonic=key, mode=scale)

        # get the index of the key in order to find its frequency in the frequency array
        idx_of_major_key = relative_major_key.get_c_based_index_of_key()
        idx_of_minor_key = relative_minor_key.get_c_based_index_of_key()

        # get the frequency of each tonic
        major_frequency = note_frequencies[idx_of_major_key]
        minor_frequency = note_frequencies[idx_of_minor_key]

        # compare and return the most common key scale
        if major_frequency >= minor_frequency:
            return relative_major_key_scale
        else:
            return relative_minor_key_scale

    def detect_key_by_phrase_endings(self):
        """
        Takes the song object and looks at the notes in the melody and bass tracks, and finds the notes with the longest
        pauses after them (likely the ends of melodic phrases). These notes are narrowed down until the set number of
        notes (as a percentage) are found.
        :return: A tuple in the format [key: Key, message: String]. This message contains lots of diagnostic information
        that explains what's going on behind the scenes, and shows a confidence value.
        """
        TIME_INTERVAL_INCREASE = 20
        PERCENTAGE_TO_FIND = 0.01

        total_song_notes = 0
        time_interval = 0
        detected_key = ""
        message = ""

        for track in self.tracks:
            total_song_notes += len(track.notes)

        total_found_notes = total_song_notes
        # total_found_notes = 0

        while total_found_notes > PERCENTAGE_TO_FIND * total_song_notes:

            total_found_notes = 0
            time_interval += TIME_INTERVAL_INCREASE

            c_indexed_total_note_frequency = [0] * NUM_NOTES
            for track in self.tracks:
                if track.tag == TagEnum.MELODY or track.tag == TagEnum.BASS:
                    c_indexed_track_note_frequency = [0] * NUM_NOTES
                    for idx, note in enumerate(track.notes):
                        if idx != len(track.notes):
                            # If this note is the last note of the song, or has a long pause after

                            # if idx == len(track.notes) - 1 \
                            #         or (track.notes[idx].time + track.notes[idx].duration) % \
                            #         (4 * self.ticks_per_beat) < time_interval:
                            if idx == len(track.notes) - 1 or track.notes[idx+1].time - note.time > time_interval:

                                total_found_notes += 1
                                c_indexed_track_note_frequency[note.c_indexed_pitch_class] += 1
                                # print(track.track_name + " time: " + str(track.notes[idx-1].time) + " pitch: " +
                                #       str(track.notes[idx-1].c_indexed_pitch_class) + " ch: " + str(track.channel))
                            # if idx == len(track.notes) - 1:
                                # print("Last note: " + str(note.c_indexed_pitch_class))
                    message += (str(c_indexed_track_note_frequency) + ": " + str(track.tag) + " - " + track.track_name
                                + "\n")
                    for i in range(12):
                        c_indexed_total_note_frequency[i] += c_indexed_track_note_frequency[i]

            message += (str(c_indexed_total_note_frequency) + ": totals"  + "\n")

            max_val = 0
            max_idx = 0
            for i in range(len(c_indexed_total_note_frequency)):
                if max_val < c_indexed_total_note_frequency[i]:
                    max_val = c_indexed_total_note_frequency[i]
                    max_idx = i
            message += ("Detected key: " + KEYS[max_idx] + "\n")
            message += ("Time interval: " + str(time_interval) + "\n")
            message += ("Found notes: " + str(total_found_notes) + "\n")
            message += ("Confidence: " + str(c_indexed_total_note_frequency[max_idx]/total_found_notes) + "\n")
            message += ("ticks per beat: " + str(self.ticks_per_beat) + "\n\n")

            detected_key = KEYS[max_idx]

        return [Key(tonic=detected_key), message]

    def get_chord_names(self):
        # It would be helpful for us here to have an accidental field on a key to know if its sharp or flat
        # That's because then you know whether to use the keys or equivalent keys array
        # I think this should work for all natural keys though
        # This also doesn't account for diminished chords
        major = [1, 4, 5]
        minor = [2, 3, 6]
        key = self.detect_key().get_c_based_index_of_key()
        for track in self.tracks:
            for chord in track.chords:
                first_note_index = chord.notes[0].c_indexed_pitch_class
                first_note_name = KEYS[chord.notes[0] % NUM_NOTES]
                distance_between_notes = KEYS[first_note_index] - KEYS[key] - 1
                if distance_between_notes in major:
                    if distance_between_notes == 5 and len(chord.notes) == 4:
                        chord.name = first_note_name + " Dominant"
                    else:
                        chord.name = first_note_name + " Major"
                else:
                    chord.name = first_note_name + " Minor"
                if len(chord.notes) == 4:
                    chord.name = chord.name + " Seventh"
