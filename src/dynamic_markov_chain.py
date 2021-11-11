from __future__ import division
from enum import Enum
import sys

from Track import Track, TagEnum
from Note import Note, NUM_NOTES
import numpy as py


class DynamicMarkovChain:

    def __init__(self, name, token_length=1):
        """Constructor for Markov Chains

        Args:
            name (String): Name of the chain
            type (String): Type of chain (TODO: to be replaced with an enumeration)
        """
        self.name = name
        self.token_length = token_length
        self.probabilities = {}

    def add_song(self, song):
        """Ingests a song and adds to the total dictionary. When all note changes are added,
        divides all elements in the dictionary by the total amount of note changes recorded and
        stores this in self.probabilities, which will give the probability matrix.

        Args:
            song (Song): Song to ingest and generate probabilities from
            num_tokens (int): Tells the amount of tokens for each pattern

        Returns:
            dict(string:[(int, int)]): Dictionary of note tokens as keys and lists of tuples with a note
            and percentage of occurrences
        """
        # Get all notes from song in one list
        all_notes = []
        for track in song.tracks:
            if not track.notes or track.tag == TagEnum.PERCUSSION:
                continue
            all_notes += track.notes
        # Get first x notes of song
        previous_pattern = str(all_notes[0].c_indexed_pitch_class)
        for i in range(1, self.token_length):
            note = all_notes[i]
            previous_pattern += " " + str(note.c_indexed_pitch_class)

        # Create dictionary
        pattern_dict = self.probabilities
        # for the rest of the song, look at next note
        for i in range(self.token_length, len(all_notes)):
            next_note = all_notes[i].c_indexed_pitch_class
            # Add that and the new note as a key/value entry.
            if pattern_dict.get(previous_pattern) is None:

                pattern_dict[previous_pattern] = [[next_note, 1]]
            else:
                found = False
                for note in pattern_dict.get(previous_pattern):
                    if note[0] == next_note:
                        note[1] = note[1] + 1
                        found = True
                        break
                if not found:

                    pattern_dict.get(previous_pattern).append([next_note, 1])

            previous_pattern = str(all_notes[i - self.token_length].c_indexed_pitch_class)
            for j in range(i - self.token_length + 1, i):
                note = all_notes[j]
                previous_pattern += " " + str(note.c_indexed_pitch_class)

        # Value would be a list of lists with note and count [(0, 1), (1, 2)]
        # If the key/value pair already exists, add one to count
        for value in pattern_dict.values():
            total = 0.0
            for note in value:
                total += note[1]
            for note in value:
                note[1] = (note[1] / total)

        self.probabilities = pattern_dict
        print(pattern_dict)
        return pattern_dict
        # Key is the same pattern, value is a list of all the percentages. [0, 0.5, 0.05, 0.25, ...]

    def generate_next_note(self, current_note_token):
        """Given a token of previous notes, this will randomly generate a new note given the percetanges from
            the markov chain object.

            Args:
                current_note_token (String): A string of 'token_length' notes in C-index

            Returns:
                int, String: An int of the next note and a string of the new pattern token.
        """
        orig_token = current_note_token
        # If this token is the end of the song, we need to begin in a new position
        if self.probabilities.get(current_note_token) is None:
            # Let's check if there are any other similar patterns in the song
            for i in range(NUM_NOTES):
                new_pattern = current_note_token[:len(current_note_token) - 2] + str(i)
                if new_pattern in list(self.probabilities.keys()):
                    current_note_token = new_pattern
                    break
            # If not, let's just randomly pick a new position to continue in the chain
            if orig_token == current_note_token:
                current_note_token = py.random.choice(list(self.probabilities.keys()))
        note_follow = self.probabilities.get(current_note_token)
        percentage = []
        # print(note_follow)
        # Create a 1-D array of the percentage of a given note with this pattern token
        for i in range(NUM_NOTES):
            found = False
            for note in note_follow:
                if i == note[0]:
                    percentage.append(note[1])
                    found = True
            if not found:
                percentage.append(0)
        # Pick a random new note with the percentages and return the note and new pattern
        print(percentage)
        next_note = py.random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 1, p=percentage)
        return next_note[0], current_note_token
        # if self.type == Type.NOTE_LENGTH:
        #     raise NotImplementedError

    def generate_pattern(self, song, num_notes):
        """Given a new song object and the number of notes to generate, this method will load that
            amount of new notes into the song using the existing markov chain.

            Args:
                song (Song): A brand new Song object
                num_notes (int): The number of notes to generate

            Returns:
                Song: The edited song object
        """
        # We are currently making every note an eighth note for easier testing
        eighth_note = int(song.ticks_per_beat / 2)
        t = Track()
        song.add_track(t)
        # Start at a random place in the markov chain
        current_token = py.random.choice(list(self.probabilities.keys()))
        current_token_array = current_token.split()
        # Add the beginning notes
        for i in range(self.token_length):
            t.add_note(Note(pitch=int(current_token_array[i]) + 35, time=i * eighth_note, duration=eighth_note))
        # Iterate through the rest of the song
        for i in range(self.token_length, num_notes):
            # Generate new note for song
            next_note_rtn = self.generate_next_note(current_token)
            next_note_tone, current_token = next_note_rtn[0], next_note_rtn[1]
            # Create the new pattern with the new note
            if self.token_length == 1:
                current_token = str(next_note_tone)
            else:
                previous_pattern = current_token.split()
                current_token = previous_pattern[1]
                for j in range(2, self.token_length):
                    current_token += " " + previous_pattern[j]
                current_token += " " + str(next_note_tone)
            next_note_tone += 36  # Bump up three octave
            if py.random.randint(0, 7):
                t.add_note(Note(pitch=next_note_tone, time=i * eighth_note, duration=eighth_note))
        return song


class Type(Enum):
    NOTE_TONE = 0
    NOTE_LENGTH = 1
    CHORD_TONE = 2
    CHORD_LENGTH = 3
