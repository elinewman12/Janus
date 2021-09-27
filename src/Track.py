import note


# Stores metadata about the track and a list of Note objects

class Track:

    def __init__(self, notes=None, controls=None, track_name=None, track_device=None, channel=0):
        if notes is None:
            notes = []
        # Control messages (and program change messages) store data about how the track should be played back,
        # but are not necessarily "events" in the file. These can occur at any point during a song
        if controls is None:
            controls = []
        self.notes = notes
        self.controls = controls
        self.track_name = track_name
        self.device_name = track_device
        self.channel = channel

    def add_note(self, note=None):
        self.notes.append(note)

    def get_c_indexed_note_frequencies(self):
        c_indexed_frequencies = [0] * Note.NUM_NOTES

        for note in self.notes:
            c_indexed_frequencies[note.c_indexed_pitch_class] += 1

        return c_indexed_frequencies


