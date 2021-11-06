from __future__ import division
from enum import Enum
import sys

from Track import Track
from Note import Note
import numpy as py


class DynamicMarkovChain:

    def __init__(self, name, type):
        """Constructor for Markov Chains

        Args:
            name (String): Name of the chain
            type (String): Type of chain (TODO: to be replaced with an enumeration)
        """
        assert isinstance(type, Type)
        self.name = name
        self.type = type
        self.probabilities = None

    def add_song(self, song, num_tokens):
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
            if not track.notes:
                continue
            all_notes += track.notes
        # Get first x notes of song
        previous_pattern = str(all_notes[0].c_indexed_pitch_class)
        for i in range(1, num_tokens):
            note = all_notes[i]
            previous_pattern += " " + str(note.c_indexed_pitch_class)

        # Create dictionary
        pattern_dict = {}
        # for the rest of the song, look at next note
        for i in range(num_tokens, len(all_notes)):
            next_note = all_notes[i].c_indexed_pitch_class
            # Add that and the new note as a key/value entry.
            if pattern_dict.get(previous_pattern) is None:
                pattern_dict[previous_pattern] = [[next_note, 1]]
            found = False
            for value in pattern_dict.values():
                for note in value:
                    if note[0] == next_note:
                        note[1] = note[1] + 1
                        found = True
                        break
                if found:
                    break
            if not found:
                pattern_dict.get(previous_pattern).append([next_note, 1])

            previous_pattern = str(all_notes[i - num_tokens].c_indexed_pitch_class)
            for j in range(i - num_tokens + 1, i):
                note = all_notes[j]
                previous_pattern += " " + str(note.c_indexed_pitch_class)
            # print(previous_pattern + "\n")

        # Value would be a list of lists with note and count [(0, 1), (1, 2)]
        # If the key/value pair already exists, add one to count
        for value in pattern_dict.values():
            total = 0.0
            for note in value:
                total += note[1]
            for note in value:
                note[1] = note[1] / total

        self.probabilities = pattern_dict
        print(pattern_dict)
        return pattern_dict
        # Key is the same pattern, value is a list of all the percentages. [0, 0.5, 0.05, 0.25, ...]

    def generate_next_note(self, current_note_token):
        if self.type == Type.NOTE_TONE:
            note_follow = self.probabilities.get(current_note_token).sort()
            percentage = []
            for note in note_follow:
                percentage.append(note[1])
            next_note = py.random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 1, p=percentage)
            return next_note[0]
        if self.type == Type.NOTE_LENGTH:
            raise NotImplementedError


class Type(Enum):
    NOTE_TONE = 0
    NOTE_LENGTH = 1
    CHORD_TONE = 2
    CHORD_LENGTH = 3
