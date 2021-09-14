import Note


# Stores metadata about the track and a list of Note objects

class Track:

    def __init__(self, notes=None, track_name=None, instrument=0):
        if notes is None:
            notes = []
        self.notes = notes
        self.track_name = track_name
        self.instrument = instrument

    def add_note(self, note=None):
        self.notes.append(note)

    def get_c_indexed_note_frequencies(self):
        c_indexed_frequencies = [0] * Note.NUM_NOTES

        for note in self.notes:
            c_indexed_frequencies[note.c_indexed_pitch_class] += 1

        return c_indexed_frequencies


