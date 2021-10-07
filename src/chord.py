from track import Track
from key import Key, KEYS
from scale import SCALE_TYPES
from note import Note, NUM_NOTES
import file_io as FileIO


class Chord:

    # Constructor, takes all fields as inputs
    def __init__(self, notes=None, name=None):
        """ Constructor for Chord class

        Args:
            notes (Note[], optional): List of notes in the chord. Defaults to None.
            name (String, optional): Name of the chord. Defaults to None.
        """        
        if notes is None:
            notes = []
        self.notes = notes
        self.name = name
