from __future__ import division
from enum import Enum
import sys

from Track import Track
from Note import Note
import numpy as py


class MarkovChain:

    def __init__(self, name, type):
        """Constructor for Markov Chains

        Args:
            name (String): Name of the chain
            type (String): Type of chain (TODO: to be replaced with an enumeration)
        """
        assert isinstance(type, Type)
        self.name = name
        self.type = type
        self.totalCt = None
        self.totals = None
        self.probabilities = None

    def add_track(self, track):
        """Ingests a track and adds to the 2d totals array. When all note changes are added,
        divides all elements in the 2d array by the total amount of note changes recorded and
        stores this in self.probabilities, which will give the probability matrix.

        Args:
            track (Track): Track to ingest and generate probabilities from

        Returns:
            int[][]: Matrix of probabilities
        """
        # Get first x notes of song
        # Create dictionary
        # for the rest of the song, look at next note
        # Make the last 3 notes a string of c_indexed_pitch_class integers
        # Add that and the new note as a key/value entry.
        # Value would be a list of tuples with note and count [(0, 1), (1, 2)]
        # If the key/value pair already exists, add one to count

        # Key is the same pattern, value is a list of all the percentages. [0, 0.5, 0.05, 0.25, ...]

    def generate_next_note(self, current_note):
        if self.type == Type.NOTE_TONE:
            next_note = py.random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 1, p=self.probabilities[current_note])
            return next_note[0]
        if self.type == Type.NOTE_LENGTH:
            raise NotImplementedError

class Type(Enum):
    NOTE_TONE = 0
    NOTE_LENGTH = 1
    CHORD_TONE = 2
    CHORD_LENGTH = 3
