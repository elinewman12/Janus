import Note
from enum import Enum

PERCUSSION_CHANNEL = 9
BASS_AVERAGE = 45


class Track:

    def __init__(self, notes=None, controls=None, track_name=None, track_device=None, chords=None, channel=0):
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
        if chords is None:
            chords = []
        # Control messages (and program change messages) store data about how the track should be played back,
        # but are not necessarily "events" in the file. These can occur at any point during a song
        if controls is None:
            controls = []
        self.notes = notes
        self.controls = controls
        self.track_name = track_name
        self.device_name = track_device
        self.channel = channel
        self.chords = chords
        self.tag = TagEnum.NONE

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

    def add_chord(self, chord=None):
        """ Adds a chord to the track array

        Args:
            chord (Chord): Note to append to the song. Defaults to None.
        """
        self.chords.append(chord)

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

    def generate_tags(self):
        """ Sets 'tag' field in the song to the appropriate tag based on its attributes
        This method assumes a track is only used for one section of a song and does not
        dramatically change roles during the song (ex, switch from guitar track to vocal
        track)

        """
        if len(self.notes) == 0:
            self.tag = TagEnum.NONE

        elif self.channel is PERCUSSION_CHANNEL:
            self.tag = TagEnum.PERCUSSION

        else:
            pitch_total = 0
            for note in self.notes:
                pitch_total += note.pitch
            if pitch_total / len(self.notes) < BASS_AVERAGE:
                self.tag = TagEnum.BASS      # If the average note pitch is lower than BASS_AVERAGE
            elif False:   # TODO: Once chords are added, count the number of chords in the track
                self.tag = TagEnum.CHORDS
            else:
                self.tag = TagEnum.MELODY    # If nothing else fits, this is likely a melody track


class TagEnum(Enum):
    NONE = 0
    MELODY = 1
    CHORDS = 2
    BASS = 3
    PERCUSSION = 4


