from Track import Track
from Key import Key, KEYS
from Scale import SCALE_TYPES
from Note import Note, NUM_NOTES
import FileIO


class Chord:

    # Constructor, takes all fields as inputs
    def __init__(self, notes=None, name=None):
        if notes is None:
            notes = []
        self.notes = notes
        self.name = name
