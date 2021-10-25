import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/Users/erinlitty/Desktop/CSC492/2021FallTeam17-DeHaan/src')

from Track import Track
from Key import Key, KEYS
from Scale import SCALE_TYPES
from Note import Note, NUM_NOTES
import FileIO as FileIO


class Chord:

    # Constructor, takes all fields as inputs
    def __init__(self, notes=None, name=None, time=0):
        if notes is None:
            notes = []
        self.notes = notes
        notes.sort(key=lambda x: x.pitch)
        self.name = name
        self.time = time
