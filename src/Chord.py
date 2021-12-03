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
        """ Constructor - Takes all fields as inputs
        Args:
            notes (Note[]): The notes in the chord
            name (string): The name of the chord
            time (int): The time in the song (in ticks) where the chord starts
        """
        if notes is None:
            notes = []
        self.notes = notes
        notes.sort(key=lambda x: x.pitch)
        self.name = name
        self.time = time

    def to_string(self):
        """ Returns a string with the c indexed pitch classes of all of the notes contained in the chord
        Returns:
            A string in the format "1 4 7"
        """
        new_string = str(self.notes[0].c_indexed_pitch_class)
        for i in range(1, len(self.notes)):
            new_string += " " + str(self.notes[i].c_indexed_pitch_class)
        return new_string

    def duplicate_chord(self):
        """
        creates a new chord object that is a duplicate of this chord object. The notes contained in the
            chord are new duplicate note objects

        Returns:
            A new duplicate chord object with the same fields as this chord object
        """
        notes = []
        for note in self.notes:
            notes.append(note.duplicate_note())
        return Chord(notes=notes, name=self.name, time=self.time)

