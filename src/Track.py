import Note


# Stores metadata about the track and a list of Note objects
class Track:

    def __init__(self, notes=None, track_name=None, instrument=0):
        if notes is None:
            notes = []
        self.notes = notes
        self.track_name = track_name
        self.instrument = instrument

    def add_note(self, n):
        self.notes.append(n)
