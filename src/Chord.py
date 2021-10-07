from track import Track
from key import Key, KEYS
from scale import SCALE_TYPES
from note import Note, NUM_NOTES
import file_io as FileIO


class Chord:

    # Constructor, takes all fields as inputs
    def __init__(self, notes=None, name=None):
        if notes is None:
            notes = []
        self.notes = notes
        self.name = name
