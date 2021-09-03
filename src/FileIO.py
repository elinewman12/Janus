import sys

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

    # -----------------------------------
    # This section prints out the input midi file to a text file called "output"
    # - Remove in final version
#    original_stdout = sys.stdout  # Save a reference to the original standard output
#
#    with open('output.txt', 'w') as f:
#        sys.stdout = f  # Change the standard output to the file we created.
#        print(midi)
#    sys.stdout = original_stdout  # Reset the standard output to its original value
    # -----------------------------------

    # File has one track with multiple channels
    if midi.type == 0:
        print("type 0")

    # File has multiple synchronous tracks
    elif midi.type == 1:

        # For each mido track in the file
        for readTrack in midi.tracks:

            # Make a new internal track representation
            track: Track = Track()
            # Notes that have had their note_on message read, but don't yet have a note_off message
            currentNotes = []
            # The current running time of the song (In absolute terms)
            currentTime = 0
            # For each message in the mido track
            for msg in readTrack:

                # Add the delay between notes to the current time
                currentTime += msg.time

                # If this message is a note and not metadata
                if hasattr(msg, 'note'):

                    # If this message is the start of a note
                    if msg.type == 'note_on':
                        # Create a new Note object and add it to the array of currently playing notes
                        currentNotes.append(Note(msg.note, currentTime, 0, msg.velocity))

                    # If this message is the end of a note
                    if msg.type == 'note_off':
                        # For each note that is currently playing
                        for n in currentNotes:
                            # Check if the pitch is the same (locate the correct note)
                            if n.pitch == msg.note:
                                # Set the duration of this note based on currentTime - start time, add it to the track
                                n.duration = currentTime - n.time
                                currentNotes.remove(n)
                                track.addNote(n)
                                break

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

