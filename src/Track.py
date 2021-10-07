import Note

PERCUSSION_CHANNEL = 9

class Track:

    def __init__(self, notes=None, controls=None, track_name=None, track_device=None, channel=0):
        """ Constructor for the Track object

        Args:
            notes (Note[], optional): List of Notes within this track. Defaults to None.
            controls (Control[], optional): List of Control messages within this track. Defaults to None.
            track_name (String, optional): Name of this track. Defaults to None.
            track_device (String, optional): Instrument used on this track. Defaults to None.
            channel (int, optional): Channel of this track. Defaults to 0.
        """        
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

        if channel is PERCUSSION_CHANNEL:
            self.is_percussion = True
        else:
            self.is_percussion = False

    def add_note(self, note=None):
        """ Adds a note to the end of this track

        Args:
            note (Note): Note to append to the song. Defaults to None.
        """        
        self.notes.append(note)

    def get_c_indexed_note_frequencies(self):
        """ Returns an array representing each note's number of appearances in this track, starting
        with C.

        Returns:
            int[]: Note frequencies array
        """        
        c_indexed_frequencies = [0] * Note.NUM_NOTES

        for note in self.notes:
            c_indexed_frequencies[note.c_indexed_pitch_class] += 1

        return c_indexed_frequencies


