from __future__ import division
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/Users/erinlitty/Desktop/CSC492/2021FallTeam17-DeHaan/src')

from Track import Track
import numpy as py

class MarkovChain:

    def __init__(self, name, type):
        """Constructor for Markov Chains

        Args:
            name (String): Name of the chain
            type (String): Type of chain (TODO: to be replaced with an enumeration)
        """        
        self.name = name
        self.type = type
        self.totalCt = py.zeros(12)
        self.totals = py.zeros((12, 12))
        self.probabilites = py.zeros((12, 12))

    def add_track(self, track):
        """Ingests a track and adds to the 2d totals array. When all note changes are added,
        divides all elements in the 2d array by the total amount of note changes recorded and
        stores this in self.probabilities, which will give the probability matrix.

        Args:
            track (Track): Track to ingest and generate probabiliites from

        Returns:
            int[][]: Matrix of probabiliites
        """        
        assert isinstance(track, Track)
        if self.type == 'note_length':
            return "Not yet implemented"
        elif self.type == 'note_tone':
            # Go through song and calculate probabilities of each note tonic based on the previous note tonic
            # Make 2D array of length 12 x 12 for each note
            for i in range(0, len(track.notes) - 1):
                self.totalCt[track.notes[i].c_indexed_pitch_class] += 1
                # Add an occurance for track.note[i] -> track.note[i+1]
                self.totals[track.notes[i].c_indexed_pitch_class, track.notes[i + 1].c_indexed_pitch_class] += 1
            # self.probabilities = self.totals / totalCt
            for idx in range(0, 12):
                if self.totalCt[idx] == 0:
                    self.totalCt[idx] = 1
                self.probabilites[idx] = self.totals[idx] / self.totalCt[idx]
            return self.probabilites
        elif self.type == 'chord_length':
            return "Not yet implemented"
        elif self.type == 'chord_tone':
            return "Not yet implemented"
