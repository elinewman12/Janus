import logging
from logging import info
from Track import Track, TagEnum
from Key import Key, KEYS
from Scale import SCALE_TYPES
from Note import NUM_NOTES
from enum import Enum
import FileIO as FileIO
import copy

# import matplotlib.pyplot as plt
import collections
# import graphviz

DEFAULT_TICKS_PER_BEAT = 48


# Stores metadata about a song, and the tracks included in the song
# <jmleeder>
class Song:

    def __init__(self, tracks=None, ticks_per_beat=DEFAULT_TICKS_PER_BEAT, key=None):
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
        if isinstance(key, Key):
            self.key = key
        else:
            self.key = None

    def add_track(self, t):
        """ Adds a new track to the song.

        Args:
            t (Track): Track to add to the song
        """
        assert isinstance(t, Track)
        self.tracks.append(t)

    def append_track(self, track_num, track):
        t = copy.deepcopy(track)
        assert isinstance(track, Track)
        prev_time = self.tracks[track_num].notes[-1].time + self.tracks[track_num].notes[-1].duration
        for note in t.notes:
            note.time += prev_time
            self.tracks[track_num].add_note(note)

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
        self.detect_key_and_scale()
        self.get_chord_names()

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

    def get_tracks_by_tag(self, tag: TagEnum):
        """
        Returns an array of tracks in the song that have the given tag attached
        :param tag: the tag enum that will be searched for
        :return: An array of tracks that match the given tag enum
        """
        tracks = []
        for track in self.tracks:
            if track.tag == tag:
                tracks.append(track)
        return tracks

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

        self.get_chord_names()
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

        self.get_chord_names()
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
            logging.info(msg="These songs have different ticks_per_beat values")
            logging.info(msg="This: " + str(self.ticks_per_beat) + ", compare to: " + str(song.ticks_per_beat))
            return False

        if len(self.tracks) != len(song.tracks):
            logging.info(msg="These songs have a different number of tracks")
            logging.info(msg="This: " + str(len(self.tracks)) + ", compare to: " + str(len(song.tracks)))
            return False

        for i, track in enumerate(self.tracks):
            if track.channel != song.tracks[i].channel:
                logging.info(msg="tracks " + str(i) + " have different channel values")
                logging.info(msg="This: " + track.channel + ", compare to: " + song.tracks[i].channel)
                return False

            if track.track_name != song.tracks[i].track_name:
                logging.info(msg="tracks " + str(i) + " have different track names :")
                logging.info(msg="This: '" + track.track_name + "', compare to: '" + song.tracks[i].track_name + "'")
                return False

            if track.device_name != song.tracks[i].device_name:
                logging.info(msg="tracks " + str(i) + " have different device names")
                logging.info(msg="This: '" + track.device_name + "', compare to: '" + song.tracks[i].device_name + "'")
                return False

            if len(track.controls) != len(song.tracks[i].controls):
                logging.info(msg="tracks " + str(i) + " have different numbers of control messages")
                logging.info(msg="This: " + str(len(track.controls)) + ", compare to: "
                                 + str(len(song.tracks[i].controls)))
                return False

            for j, control in enumerate(track.controls):
                if control.msg_type != song.tracks[i].controls[j].msg_type:
                    logging.info(msg="tracks " + str(i) + " control " + str(j) + " have different message types")
                    logging.info(msg="This: '" + control.msg_type + "', compare to: '"
                                     + song.tracks[i].controls[j].msg_type + "'")
                    return False

                if control.control != song.tracks[i].controls[j].control:
                    logging.info(msg="tracks " + str(i) + " control " + str(j) + " have different control numbers")
                    logging.info(msg="This: " + str(control.control) + ", compare to: "
                                     + str(song.tracks[i].controls[j].control))
                    return False

                if control.value != song.tracks[i].controls[j].value:
                    logging.info(msg="tracks " + str(i) + " control " + str(j) + " have different values")
                    logging.info(msg="This: " + str(control.value) + ", compare to: "
                                     + str(song.tracks[i].controls[j].value))
                    return False

                if control.tempo != song.tracks[i].controls[j].tempo:
                    logging.info(msg="tracks " + str(i) + " control " + str(j) + " have different tempos")
                    logging.info(msg="This: " + str(control.tempo) + ", compare to: "
                                     + str(song.tracks[i].controls[j].tempo))
                    return False

                if control.instrument != song.tracks[i].controls[j].instrument:
                    logging.info(msg="tracks " + str(i) + " control " + str(j) + " have different instruments")
                    logging.info(msg="This: " + str(control.instrument) + ", compare to: " + str(
                        song.tracks[i].controls[j].instrument))
                    return False

                if control.time != song.tracks[i].controls[j].time:
                    logging.info(msg="tracks " + str(i) + " control " + str(j) + " have different times")
                    logging.info(msg="This: " + str(control.time) + ", compare to: "
                                     + str(song.tracks[i].controls[j].time))
                    return False

            if len(track.notes) != len(song.tracks[i].notes):
                logging.info(msg="tracks " + str(i) + " have different numbers of notes")
                logging.info(msg="This: " + str(len(track.notes)) + ", compare to: " + str(len(song.tracks[i].notes)))
                return False

            for j, note in enumerate(track.notes):
                if note.pitch != song.tracks[i].notes[j].pitch:
                    logging.info(msg="tracks " + str(i) + " note " + str(j) + " have different pitches")
                    logging.info(msg="This: " + str(note.pitch) + ", compare to: " + str(song.tracks[i].notes[j].pitch))
                    return False

                if note.time != song.tracks[i].notes[j].time:
                    logging.info(msg="tracks " + str(i) + " note " + str(j) + " have different times")
                    logging.info(msg="This: " + str(note.time) + ", compare to: " + str(song.tracks[i].notes[j].time))
                    return False

                if note.duration != song.tracks[i].notes[j].duration:
                    logging.info(msg="tracks " + str(i) + " note " + str(j) + " have different durations")
                    logging.info(msg="This: " + str(note.duration) + ", compare to: "
                                     + str(song.tracks[i].notes[j].duration))
                    return False

                if note.velocity != song.tracks[i].notes[j].velocity:
                    logging.info(msg="tracks " + str(i) + " note " + str(j) + " have different velocities")
                    logging.info(msg="This: " + str(note.velocity) + ", compare to: "
                                     + str(song.tracks[i].notes[j].velocity))
                    return False

                if note.channel != song.tracks[i].notes[j].channel:
                    logging.info(msg="tracks " + str(i) + " note " + str(j) + " have different channels")
                    logging.info(msg="This: " + str(note.channel) + ", compare to: "
                                     + str(song.tracks[i].notes[j].channel))
                    return False

        return True

    def generate_possible_keys_and_scales(self):
        """ 
        Detect the key of a song using Mr. Dehaan's algorithm.  This algorithm generates the valid notes
        for every key and for every scale and checks the occurrences of the notes in the song against the valid
        key/scale notes.  It then finds how many errors (or misses) occurred.  It then finds the key/scale with the
        lowest number of errors (or the list of key/scale with the same minimum) and returns the result.
        :return: A list of Key objects that have the minimum number of errors [0], and the minimum errors [1]
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

        keys = []
        for key in result:
            keys.append(Key(key.split()[0], key.split()[1]))

        return keys, minimum_errors

    def detect_key_and_scale(self):
        """
        Uses the generate possible keys and scales method to get a list of potential keys, determines which is
        the most likely based on the most common notes in the song.

        :return: The detected key [0], the minimum errors [1], and the confidence level [2]
        """

        note_frequencies = self.get_c_indexed_note_frequencies()
        num_notes = sum(note_frequencies)
        keys, minimum_errors = self.generate_possible_keys_and_scales()


        # now we have the relative major and minors, we can use the note frequencies to differentiate
        # between the two based on the assumption that for most cases the tonic will be played more than
        # other notes.  This lets us differentiate scales with the same notes such as D major and B Minor.

        # get the resulting keys/scales
        relative_major_key_scale = None
        relative_minor_key_scale = None
        for key in keys:
            if key.mode == "major":
                relative_major_key_scale = key
            elif key.mode == "minor":
                relative_minor_key_scale = key

        # get the index of the key in order to find its frequency in the frequency array
        idx_of_major_key = relative_major_key_scale.get_c_based_index_of_key()
        idx_of_minor_key = relative_minor_key_scale.get_c_based_index_of_key()

        # get the frequency of each tonic
        major_frequency = note_frequencies[idx_of_major_key]
        minor_frequency = note_frequencies[idx_of_minor_key]

        # compare and return the most common key scale
        if major_frequency >= minor_frequency:
            detected_return_key = relative_major_key_scale
        else:
            detected_return_key = relative_minor_key_scale

        # determine confidence based on number of 1 - number of errors/ number of notes
        confidence = 1 - minimum_errors / num_notes

        # set the key of the song
        self.key = detected_return_key

        # return the tuple
        return detected_return_key, minimum_errors, confidence

    def detect_key_by_phrase_endings(self):
        """
        Takes the song object and looks at the notes in the melody and bass tracks, and finds the notes with the longest
        pauses after them (likely the ends of melodic phrases). These notes are narrowed down until the set number of
        notes (as a percentage) are found.
        :return: Three objects in the format [key: Key, message: String, confidence: String]. The message contains
        lots of diagnostic information that explains what's going on behind the scenes, and shows a confidence value.
        Note: If the detected tonic is not a note in the detected scale,
        """
        TIME_INTERVAL_INCREASE = 20
        PERCENTAGE_TO_FIND = 0.01

        total_song_notes = 0
        time_interval = 0
        detected_tonic = ""
        message = ""
        confidence = ""

        for track in self.tracks:
            total_song_notes += len(track.notes)

        total_found_notes = total_song_notes
        # total_found_notes = 0

        # Until you find less than the percentage in PERCENTAGE_TO_FIND
        while total_found_notes > PERCENTAGE_TO_FIND * total_song_notes and total_found_notes > len(self.tracks):

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
                    message += (str(c_indexed_track_note_frequency) + ": " + str(track.tag) + " - " +
                                str(track.track_name) + "\n")
                    for i in range(12):
                        c_indexed_total_note_frequency[i] += c_indexed_track_note_frequency[i]

            message += (str(c_indexed_total_note_frequency) + ": totals"  + "\n")

            max_val = 0
            max_idx = -1
            for i in range(len(c_indexed_total_note_frequency)):
                if max_val < c_indexed_total_note_frequency[i]:
                    max_val = c_indexed_total_note_frequency[i]
                    max_idx = i

            if total_found_notes == 0:
                confidence = 0
            else:
                confidence = str(c_indexed_total_note_frequency[max_idx] / total_found_notes)

            message += ("Detected key: " + KEYS[max_idx] + "\n")
            message += ("Time interval: " + str(time_interval) + "\n")
            message += ("Found notes: " + str(total_found_notes) + "\n")
            message += ("Confidence: " + confidence + "\n")
            message += ("ticks per beat: " + str(self.ticks_per_beat) + "\n\n")

            # The detected tonic of the song (NOT a Key object yet)
            detected_tonic = KEYS[max_idx]

        # Convert detected_key into a Key object with the correct scale
        possible_keys = self.generate_possible_keys_and_scales()[0]
        detected_key = None
        for key in possible_keys:
            if key.tonic == detected_tonic:
                detected_key = key

        # If the detected tonic is not in the list of possible keys, choose the major mode of the detected scale.
        if detected_key is None:
            for key in possible_keys:
                if key.mode == 'major':
                    detected_key = key

        # set the key of the song
        self.key = detected_key

        return [detected_key, message, confidence]

    def get_chord_names(self):
        # It would be helpful for us here to have an accidental field on a key to know if its sharp or flat
        # That's because then you know whether to use the keys or equivalent keys array
        # I think this should work for all natural keys though
        # This also doesn't account for diminished chords
        major = [1, 4, 5]
        minor = [2, 3, 6]
        # Gets the key of the song, as an integer
        key = self.key.get_c_based_index_of_key()
        # Iterate over every chord in every track
        for track in self.tracks:
            for chord in track.chords:
                # Get the name of the first note in the chord which will
                # commonly be the name of the chord.
                first_note_index = chord.notes[0].c_indexed_pitch_class
                first_note_name = KEYS[chord.notes[0].pitch % NUM_NOTES]
                # The distance between our first note and the key will tell
                # us if its major or minor.
                distance_between_notes = first_note_index - key + 1
                if distance_between_notes in major:
                    if distance_between_notes == 5 and len(chord.notes) == 4:
                        chord.name = first_note_name + " Dominant"
                    else:
                        chord.name = first_note_name + " Major"
                else:
                    chord.name = first_note_name + " Minor"
                if len(chord.notes) == 4:
                    chord.name = chord.name + " Seventh"

    def get_transition_graph(self, name):
        # TODO: Change the way it iterates through tracks so the chords are always connected by the time
        # they occur in the song.
        # Create a directed graph object and set dimensions
        graph = graphviz.Digraph(comment="Chord transitions in Song")
        graph.attr(ranksep='0.01', nodesep='0.1', label=name + " Chord Transitions", labelloc="t")
        chord_set = set()
        edges = []
        all_chords = []
        # Iterate over every track in song
        for track in self.tracks:
            if not track.chords:
                continue
            all_chords += track.chords

        all_chords.sort(key=lambda chord: chord.time)
        # Hold the previous chord
        prev_chord = all_chords[0]
        graph.node(prev_chord.name)
        chord_set.add(prev_chord.name)
        # Iterate over every chord in track
        for i in range(1, len(all_chords)):
            curr = all_chords[i]
            # Only add chords that are not already on graph
            if curr.name not in chord_set:
                graph.node(curr.name)
                chord_set.add(curr.name)
            edges.append([prev_chord.name, curr.name])
            print(prev_chord.name + " -> " + curr.name)
            prev_chord = curr

        counter = collections.Counter(tuple(edge) for edge in edges)
        for edge, count in counter.items():
            # print(str(edge[0]), count)
            graph.edge(str(edge[0]), str(edge[1]), label=str(count))
        graph.view()

class SongLibrary(str, Enum):
    GARTH_BROOKS_FRIENDS_IN_LOW_PLACES = "MIDI Files/Country/Garth Brooks/23224_Friends-in-Low-Places.mid"
    GARTH_BROOKS_TO_MAKE_YOU_FEEL_MY_LOVE = "MIDI Files/Country/Garth Brooks/26553_To-Make-You-Feel-My-Love.mid"
    JOHN_ANDERSON_I_WISH_I_COULD_HAVE_BEEN_THERE = "MIDI Files/Country/John Anderson/2601_I-Wish-I-Could-Have-Been-There.mid"
    JOHN_ANDERSON_SEMINOLE_WIND = "MIDI Files/Country/John Anderson/2603_Seminole-Wind.mid"
    TIM_MCGRAW_DONT_TAKE_THE_GIRL = "MIDI Files/Country/Tim McGraw/1576_Dont-Take-the-Girl.mid"
    TIM_MCGRAW_I_LIKE_IT_I_LOVE_IT = "MIDI Files/Country/Tim McGraw/1577_I-Like-It-I-Love-It.mid"
    TIM_MCGRAW_SOMETHING_LIKE_THAT = "MIDI Files/Country/Tim McGraw/2610_Something-Like-That.mid"
    ALAN_WALKER_ALONE = "MIDI Files/EDM/Alan Walker/Alan Walker - Alone  (midi by Carlo Prato) (www.cprato.com).mid"
    ALAN_WALKER_FADED = "MIDI Files/EDM/Alan Walker/Alan Walker - Faded (Piano Cover Tutorial - Easy) (midi by Carlo Prato) (www.cprato.com).mid"
    ALAN_WALKER_SING_ME_TO_SLEEP = "MIDI Files/EDM/Alan Walker/Alan Walker - Sing Me To Sleep  (midi by Carlo Prato) (www.cprato.com).mid"
    DEADMAU5_2448 = "MIDI Files/EDM/Deadmau5/deadmau5 - 2448  (midi by Carlo Prato) (www.cprato.com).mid"
    DEADMAU5_DEUS_EX_MACHINA = "MIDI Files/EDM/Deadmau5/deadmau5 - Deus Ex Machina  (midi by Carlo Prato) (www.cprato.com).mid"
    DEADMAU5_HYPERLANDIA = "MIDI Files/EDM/Deadmau5/deadmau5 - Hyperlandia  (midi by Carlo Prato) (www.cprato.com).mid"
    DEADMAU5_NO_PROBLEM = "MIDI Files/EDM/Deadmau5/deadmau5 - No Problem  (midi by Carlo Prato) (www.cprato.com).mid"
    DEADMAU5_SO_THERE_I_WAS = "MIDI Files/EDM/Deadmau5/deadmau5 - So There I Was  (midi by Carlo Prato) (www.cprato.com).mid"
    DEADMAU5_FT_GRABBITZ_LET_GO = "MIDI Files/EDM/Deadmau5/deadmau5 feat. Grabbitz - Let Go  (midi by Carlo Prato) (www.cprato.com).mid"
    MARSHMELLO_ALONE = "MIDI Files/EDM/Marshmello/Marshmello - Alone (Original Mix) (midi by Carlo Prato) (www.cprato.com).mid"
    MARSHMELLO_RITUAL = "MIDI Files/EDM/Marshmello/Marshmello - Ritual (Original Mix) (midi by Carlo Prato) (www.cprato.com).mid"
    MARSHMELLO_SUMMER = "MIDI Files/EDM/Marshmello/Marshmello - Summer  (midi by Carlo Prato) (www.cprato.com).mid"
    MARTIN_GARRIX_FT_BEBE_REXHA_IN_THE_NAME_OF_LOVE = "MIDI Files/EDM/Martin Garrix/Martin Garrix & Bebe Rexha - In The Name Of Love  (midi by Carlo Prato) (www.cprato.com).mid"
    MARTIN_GARRIX_FT_DUA_LIPA_SCARED_TO_BE_LONELY = "MIDI Files/EDM/Martin Garrix/Martin Garrix & Dua Lipa - Scared To Be Lonely  (midi by Carlo Prato) (www.cprato.com).mid"
    MARTIN_GARRIX_FT_THE_FEDERAL_EMPIRE_HOLD_ON_AND_BELIEVE = "MIDI Files/EDM/Martin Garrix/Martin Garrix ft. The Federal Empire - Hold On & Believe (Original Mix) (midi by Carlo Prato) (www.cprato.com).mid"
    JOHN_NEWTON_AMAZING_GRACE = "MIDI Files/Gospel/John Newton/Amazing_Grace.mid"
    NIRVANA_ABOUT_A_GIRL = "MIDI Files/Grunge/Nirvana/AboutAGirl.mid"
    NIRVANA_COME_AS_YOU_ARE = "MIDI Files/Grunge/Nirvana/ComeAsYouAre.mid"
    NIRVANA_HEART_SHAPED_BOX = "MIDI Files/Grunge/Nirvana/HeartShapedBox.mid"
    NIRVANA_IN_BLOOM = "MIDI Files/Grunge/Nirvana/InBloom.mid"
    NIRVANA_LITHIUM = "MIDI Files/Grunge/Nirvana/Lithium.mid"
    NIRVANA_SMELLS_LIKE_TEEN_SPIRIT = "MIDI Files/Grunge/Nirvana/SmellsLikeTeenSpirit.mid"
    PEARL_JAM_ALIVE = "MIDI Files/Grunge/Pearl Jam/Alive.mid"
    PEARL_JAM_BETTER_MAN = "MIDI Files/Grunge/Pearl Jam/BetterMan.mid"
    PEARL_JAM_EVEN_FLOW = "MIDI Files/Grunge/Pearl Jam/EvenFlow.mid"
    PEARL_JAM_JEREMY = "MIDI Files/Grunge/Pearl Jam/Jeremy.mid"
    PEARL_JAM_YELLOW_LEDBETTER = "MIDI Files/Grunge/Pearl Jam/YellowLedbetter.mid"
    SOUNDGARDEN_BLACK_HOLE_SUN = "MIDI Files/Grunge/Soundgarden/BlackHoleSun.mid"
    SOUNDGARDEN_SPOON_MAN = "MIDI Files/Grunge/Soundgarden/SpoonMan.mid"
    STONE_TEMPLE_PILOTS_CREEP = "MIDI Files/Grunge/Stone Temple Pilots/Creep.mid"
    STONE_TEMPLE_PILOTS_INTERSTATE_LOVE_SONG = "MIDI Files/Grunge/Stone Temple Pilots/InterstateLoveSong.mid"
    STONE_TEMPLE_PILOTS_PLUSH = "MIDI Files/Grunge/Stone Temple Pilots/Plush.mid"
    STONE_TEMPLE_PILOTS_TRIPPING_ON_A_HOLE = "MIDI Files/Grunge/Stone Temple Pilots/TrippingOnAHole.mid"
    STONE_TEMPLE_PILOTS_VASOLINE = "MIDI Files/Grunge/Stone Temple Pilots/Vasoline.mid"
    CHANCE_THE_RAPPER_ALL_WE_GOT_FOR_MARCHING_BAND = "MIDI Files/Hip-Hop/Chance The Rapper/Chance_the_Rapper_-_All_We_Got_for_Marching_Band.mid"
    CHANCE_THE_RAPPER_NO_PROBLEM = "MIDI Files/Hip-Hop/Chance The Rapper/NO_PROBLEM.mid"
    CHANCE_THE_RAPPER_SUNDAY_CANDY = "MIDI Files/Hip-Hop/Chance The Rapper/Sunday_Candy_G_Major_Final.mid"
    EMINEM_LOSE_YOURSELF = "MIDI Files/Hip-Hop/Eminem/20455_Lose-Yourself.mid"
    EMINEM_MARSHALL_MATHERS = "MIDI Files/Hip-Hop/Eminem/20501_Marshall-Mathers.mid"
    EMINEM_MY_NAME_IS = "MIDI Files/Hip-Hop/Eminem/23214_My-Name-Is.mid"
    EMINEM_THE_REAL_SLIM_SHADY = "MIDI Files/Hip-Hop/Eminem/27297_Real-Slim-Shady-The.mid"
    JAY_Z_BIG_PIMPIN = "MIDI Files/Hip-Hop/Jay-Z/13235_Big-Pimpin.mid"
    JAY_Z_HARD_KNOCK_LIFE = "MIDI Files/Hip-Hop/Jay-Z/13238_Hard-Knock-Life.mid"
    JAY_Z_BONNIE_CLYDE = "MIDI Files/Hip-Hop/Jay-Z/20535_03-Bonnie--Clyde.mid"
    KANYE_WEST_ALL_FALLS_DOWN = "MIDI Files/Hip-Hop/Kanye West/21530_All-Falls-Down.mid"
    KANYE_WEST_JESUS_WALKS = "MIDI Files/Hip-Hop/Kanye West/24774_Jesus-Walks.mid"
    KANYE_WEST_GOLD_DIGGER = "MIDI Files/Hip-Hop/Kanye West/24851_Gold-Digger.mid"
    NOTORIOUS_BIG_MISS_U = "MIDI Files/Hip-Hop/Notorious B.I.G/13224_Miss-U.mid"
    NOTORIOUS_BIG_MO_MONEY_MO_PROBLEMS = "MIDI Files/Hip-Hop/Notorious B.I.G/13225_Mo-Money-Mo-Problems.mid"
    NOTORIOUS_BIG_ONE_MORE_CHANCE = "MIDI Files/Hip-Hop/Notorious B.I.G/13227_One-More-Chance.mid"
    OUTKAST_HEY_YA = "MIDI Files/Hip-Hop/OutKast/20700_Hey-Ya.mid"
    OUTKAST_MISS_JACKSON = "MIDI Files/Hip-Hop/OutKast/21165_Miss-Jackson.mid"
    OUTKAST_ROSES = "MIDI Files/Hip-Hop/OutKast/25535_Roses.mid"
    SIMON_AND_GARFUNKEL_SCARBOROUGH_FAIR = "MIDI Files/Indie/Simon and Garfunkel/scarborough_fair.mid"
    FRANK_SINATRA_MY_WAY = "MIDI Files/Jazz/Frank Sinatra/my_way.mid"
    BLACK_SABBATH_IRON_MAN = "MIDI Files/Metal/Black Sabbath/Black Sabbath-Iron Man.mid"
    BLACK_SABBATH_PARANOID = "MIDI Files/Metal/Black Sabbath/Black Sabbath-Paranoid.mid"
    BLACK_SABBATH_WAR_PIGS = "MIDI Files/Metal/Black Sabbath/Black Sabbath-War pigs.mid"
    JUDAS_PRIEST_GRINDER = "MIDI Files/Metal/Judas Priest/Judas Priest - Grinder.mid"
    JUDAS_PRIEST_LIVING_AFTER_MIDNIGHT = "MIDI Files/Metal/Judas Priest/Judas Priest - Living after Midnight.mid"
    JUDAS_PRIEST_NIGHT_CRAWLER = "MIDI Files/Metal/Judas Priest/Judas Priest - Night Crawler.mid"
    MEGADETH_HOLY_WARS_THE_PUNISHMENT_DUE = "MIDI Files/Metal/Megadeth/Megadeth-Holy Wars The Punishment Due.mid"
    MEGADETH_SYMPHONY_OF_DESTRUCTION = "MIDI Files/Metal/Megadeth/Megadeth-Symphony Of Destruction.mid"
    MEGADETH_TORNADO_OF_SOULS = "MIDI Files/Metal/Megadeth/Megadeth-Tornado Of Souls.mid"
    METALLICA_ENTER_SANDMAN = "MIDI Files/Metal/Metallica/EnterSandman.mid"
    ADELE_SET_FIRE_TO_THE_RAIN = "MIDI Files/Pop/Adele/Adele_-_Set_fire_to_the_rain.mid"
    ADELE_SKYFALL = "MIDI Files/Pop/Adele/Adele_-_Skyfall.mid"
    ADELE_MAKE_YOU_FEEL_MY_LOVE = "MIDI Files/Pop/Adele/adele-make_you_feel_my_love.mid"
    ADELE_SOMEONE_LIKE_YOU = "MIDI Files/Pop/Adele/adele-someone_like_you.mid"
    ADELE_LOVE_IN_THE_DARK = "MIDI Files/Pop/Adele/Love in the Dark.mid"
    BILLIE_EILISH_ALL_THE_GOOD_GIRLS_GO_TO_HELL = "MIDI Files/Pop/Billie Eilish/Billie Eilish - All The Good Girls Go To Hell  (midi by Carlo Prato) (www.cprato.com).mid"
    BILLIE_EILISH_BAD_GUY = "MIDI Files/Pop/Billie Eilish/Billie Eilish - Bad Guy  (midi by Carlo Prato) (www.cprato.com).mid"
    BILLIE_EILISH_NO_TIME_TO_DIE = "MIDI Files/Pop/Billie Eilish/Billie Eilish - No Time To Die (James Bond) (midi by Carlo Prato) (www.mid"
    BILLIE_EILISH_THEREFORE_I_AM = "MIDI Files/Pop/Billie Eilish/Billie Eilish - Therefore I Am- (midi by Carlo Prato) (www.cprato.com).mid"
    BRUNO_MARS_GRENADE = "MIDI Files/Pop/Bruno Mars/Grenade.mid"
    BRUNO_MARS_RUNAWAY_BABY = "MIDI Files/Pop/Bruno Mars/RunawayBaby.mid"
    BRUNO_MARS_THE_LAZY_SONG = "MIDI Files/Pop/Bruno Mars/Thelazysong.mid"
    ED_SHEERAN_GALWAY_GIRL = "MIDI Files/Pop/Ed Sheeran/Ed Sheeran - Galway Girl  (midi by Carlo Prato) (www.cprato.com).mid"
    ED_SHEERAN_PERFECT = "MIDI Files/Pop/Ed Sheeran/Ed Sheeran - Perfect  (midi by Carlo Prato) (www.cprato.com).mid"
    ED_SHEERAN_SHAPE_OF_YOU = "MIDI Files/Pop/Ed Sheeran/Ed Sheeran - Shape of You  (midi by Carlo Prato) (www.cprato.com).mid"
    IMAGINE_DRAGONS_BELIEVER = "MIDI Files/Pop/Imagine Dragons/Believer_-_Imagine_Dragons.mid"
    IMAGINE_DRAGONS_DEMONS = "MIDI Files/Pop/Imagine Dragons/Demons_-_Imagine_Dragons.mid"
    IMAGINE_DRAGONS_RADIOACTIVE = "MIDI Files/Pop/Imagine Dragons/Radioactive.mid"
    THE_CHAINSMOKERS_PARIS = "MIDI Files/Pop/The Chainsmokers/The Chainsmokers - Paris  (midi by Carlo Prato) (www.cprato.com).mid"
    THE_CHAINSMOKERS_FT_XYLO_SETTING_FIRES = "MIDI Files/Pop/The Chainsmokers/The Chainsmokers feat. XYLØ - Setting Fires  (midi by Carlo Prato) (www.cprato.com).mid"
    THE_CHAINSMOKERS_FT_HALSEY_CLOSER = "MIDI Files/Pop/The Chainsmokers/The Chainsmokers ft. Halsey - Closer  (midi by Carlo Prato) (www.cprato.com).mid"
    THE_CHAINSMOKERS_FT_PHOEBE_RYAN_ALL_WE_KNOW = "MIDI Files/Pop/The Chainsmokers/The Chainsmokers ft. Phoebe Ryan - All We Know  (midi by Carlo Prato) (www.cprato.com).mid"
    THE_WEEKND_PARTY_MONSTER = "MIDI Files/Pop/The Weeknd/The Weeknd - Party Monster  (midi by Carlo Prato) (www.cprato.com).mid"
    THE_WEEKND_REMINDER = "MIDI Files/Pop/The Weeknd/The Weeknd - Reminder  (midi by Carlo Prato) (www.cprato.com).mid"
    THE_WEEKND_FT_DAFT_PUNK_I_FEEL_IT_COMING = "MIDI Files/Pop/The Weeknd/The Weeknd ft. Daft Punk - I Feel It Coming  (midi by Carlo Prato) (www.cprato.com).mid"
    AEROSMITH_COME_TOGETHER = "MIDI Files/Rock/Aerosmith/ComeTogether.mid"
    AEROSMITH_DREAM_ON = "MIDI Files/Rock/Aerosmith/DreamOn.mid"
    AEROSMITH_JANIES_GOT_A_GUN = "MIDI Files/Rock/Aerosmith/JaniesGotAGun.mid"
    EAGLES_HOTEL_CALIFORNIA = "MIDI Files/Rock/Eagles/HotelCalifornia.mid"
    EAGLES_HOW_LONG = "MIDI Files/Rock/Eagles/HowLong.mid"
    EAGLES_TAKE_IT_EASY = "MIDI Files/Rock/Eagles/TakeItEasy.mid"
    ELTON_JOHN_ROCKET_MAN = "MIDI Files/Rock/Elton John/RocketMan.mid"
    ELTON_JOHN_TINY_DANCER = "MIDI Files/Rock/Elton John/TinyDancer.mid"
    ELTON_JOHN_YOUR_SONG = "MIDI Files/Rock/Elton John/YourSong.mid"
    FALL_OUT_BOY_LIGHT_EM_UP = "MIDI Files/Rock/Fall Out Boy/LightEmUp.mid"
    FALL_OUT_BOY_SUGAR_WERE_GOING_DOWN = "MIDI Files/Rock/Fall Out Boy/SugarWereGoingDown(2).mid"
    GREENDAY_BOULEVARD_OF_BROKEN_DREAMS = "MIDI Files/Rock/Greenday/BoulevardofBrokenDreams.mid"
    GREENDAY_GOOD_RIDDANCE = "MIDI Files/Rock/Greenday/GoodRiddance(TimeOfYourLife).mid"
    ROLLING_STONES_PAINT_IT_BLACK = "MIDI Files/Rock/Rolling Stones/PaintItBlack.mid"
    ROLLING_STONES_SATISFACTION = "MIDI Files/Rock/Rolling Stones/Satisfaction.mid"
    U2_I_STILL_HAVENT_FOUND_WHAT_IM_LOOKING_FOR = "MIDI Files/Rock/U2/IStillHavntFoundWhatImLookingFor.mid"
    U2_WITH_OR_WITHOUT_YOU = "MIDI Files/Rock/U2/WithorWithoutYou.mid"

# For demo branch
class SongLibrary(str, Enum):
    GARTH_BROOKS_TO_MAKE_YOU_FEEL_MY_LOVE = "MIDI Files/Country/Garth Brooks/26553_To-Make-You-Feel-My-Love.mid"
    JOHN_ANDERSON_I_WISH_I_COULD_HAVE_BEEN_THERE = "MIDI Files/Country/John Anderson/2601_I-Wish-I-Could-Have-Been-There.mid"
    TIM_MCGRAW_SOMETHING_LIKE_THAT = "MIDI Files/Country/Tim McGraw/2610_Something-Like-That.mid"
    NIRVANA_LITHIUM = "MIDI Files/Grunge/Nirvana/Lithium.mid"
    PEARL_JAM_BETTER_MAN = "MIDI Files/Grunge/Pearl Jam/BetterMan.mid"
    SOUNDGARDEN_BLACK_HOLE_SUN = "MIDI Files/Grunge/Soundgarden/BlackHoleSun.mid"
    STONE_TEMPLE_PILOTS_CREEP = "MIDI Files/Grunge/Stone Temple Pilots/Creep.mid"
    SIMON_AND_GARFUNKEL_SCARBOROUGH_FAIR = "MIDI Files/Indie/Simon and Garfunkel/scarborough_fair.mid"
    FRANK_SINATRA_MY_WAY = "MIDI Files/Jazz/Frank Sinatra/my_way.mid"
    BLACK_SABBATH_IRON_MAN = "MIDI Files/Metal/Black Sabbath/Black Sabbath-Iron Man.mid"
    JUDAS_PRIEST_NIGHT_CRAWLER = "MIDI Files/Metal/Judas Priest/Judas Priest - Night Crawler.mid"
    MEGADETH_SYMPHONY_OF_DESTRUCTION = "MIDI Files/Metal/Megadeth/Megadeth-Symphony Of Destruction.mid"
    METALLICA_ENTER_SANDMAN = "MIDI Files/Metal/Metallica/EnterSandman.mid"
    ADELE_SKYFALL = "MIDI Files/Pop/Adele/Adele_-_Skyfall.mid"
    BILLIE_EILISH_NO_TIME_TO_DIE = "MIDI Files/Pop/Billie Eilish/Billie Eilish - No Time To Die (James Bond) (midi by Carlo Prato) (www.mid"
    BRUNO_MARS_THE_LAZY_SONG = "MIDI Files/Pop/Bruno Mars/Thelazysong.mid"
    ED_SHEERAN_SHAPE_OF_YOU = "MIDI Files/Pop/Ed Sheeran/Ed Sheeran - Shape of You  (midi by Carlo Prato) (www.cprato.com).mid"
    IMAGINE_DRAGONS_RADIOACTIVE = "MIDI Files/Pop/Imagine Dragons/Radioactive.mid"
    THE_CHAINSMOKERS_FT_HALSEY_CLOSER = "MIDI Files/Pop/The Chainsmokers/The Chainsmokers ft. Halsey - Closer  (midi by Carlo Prato) (www.cprato.com).mid"
    THE_WEEKND_PARTY_MONSTER = "MIDI Files/Pop/The Weeknd/The Weeknd - Party Monster  (midi by Carlo Prato) (www.cprato.com).mid"
    AEROSMITH_DREAM_ON = "MIDI Files/Rock/Aerosmith/DreamOn.mid"
    EAGLES_HOTEL_CALIFORNIA = "MIDI Files/Rock/Eagles/HotelCalifornia.mid"
    ELTON_JOHN_ROCKET_MAN = "MIDI Files/Rock/Elton John/RocketMan.mid"
    FALL_OUT_BOY_LIGHT_EM_UP = "MIDI Files/Rock/Fall Out Boy/LightEmUp.mid"
    GREENDAY_BOULEVARD_OF_BROKEN_DREAMS = "MIDI Files/Rock/Greenday/BoulevardofBrokenDreams.mid"
    ROLLING_STONES_SATISFACTION = "MIDI Files/Rock/Rolling Stones/Satisfaction.mid"