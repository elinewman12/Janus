import Note


# Stores metadata about the track and a list of Note objects
class Track:
    # A list of notes in the song
    notes = []
    # The instrument being played on this track, stored as a string, probably?
    instrument = "instr"

    def addNote(self, n):
        self.notes.append(n)
