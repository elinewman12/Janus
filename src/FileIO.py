from mido import MidiFile
from Song import Song
from Track import Track
from Note import Note


# Takes a file name as input, creates a list of tracks, gets
# the metadata for the song, and creates a "song" object
#
# <jmleeder>
def read_midi_file(file_name):
    midi = MidiFile(file_name)
    song: Song = Song()
    # File has one track with multiple channels
    if midi.type == 0:
        print("type 0")

    # File has multiple synchronous tracks
    elif midi.type == 1:

        # For each mido track in the file
        for readTrack in midi.tracks:

            # Make a new internal track representation
            track: Track = Track()
            # For each message in the mido track
            for msg in readTrack:

                # If this message is a note and not metadata
                if hasattr(msg, 'note'):

                    # Create a new Note object and add it to the Track object we made earlier
                    note: Note = Note(msg.note, msg.time, msg.velocity)
                    track.addNote(note)

            # Add this track and its associated notes to the song
            song.addTrack(track)
        return song

    # File has multiple asynchronous tracks
    else:
        print("type 2")


# Takes a file name as input and a song as input,
# recreates a midi file using the tracks and metadata included
# in the song object
#
# <jmleeder>
def write_midi_file(self, file_name, song):
    print("Not implemented yet")

