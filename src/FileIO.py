import sys

import mido
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

    song.ticks_per_beat = midi.ticks_per_beat

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

            # Add this track and its associated notes to the song (sorted by time)
            track.notes.sort(key=lambda note: note.time)
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
def write_midi_file(file_name, song):
    # Generate new type 1 midi file with the original song's metadata
    midi = MidiFile(type=1)
    midi.ticks_per_beat = song.ticks_per_beat

    # For each track in the song
    for t in song.tracks:
        # Get an ordered list of messages
        msgs = orderMessages(t)
        # Create a new midi track and add these messages to the track
        midi.add_track(name=None)
        for m in msgs:
            midi.tracks[midi.tracks.__len__() - 1].append(m)
    # Save this midi file
    midi.save(file_name)


# Takes a track as input and returns an ordered list of midi messages.
# These messages consist of note_on and note_off messages, and will
# have their attributes (channel, pitch, velocity, time) set correctly
# based on the values stored in each note object
#
# <jmleeder>
def orderMessages(track):
    noteOn = []
    noteOff = []
    msgs = []
    time = 0

    # Generate two lists (noteOn and noteOff) that store the absolute
    # times when each note starts and ends. These lists consist of tuples,
    # [Note, int] that stores a note and it's corresponding time (either
    # starting or ending time)
    for n in track.notes:
        noteOn.append([n, n.time])
        noteOff.append([n, n.time + n.duration])

    # noteOn will be sorted inside the track object, noteOff may not be in the same order
    noteOff.sort(key=lambda note: note[1])

    # Compare the first element of the noteOn and noteOff lists. Write which ever one comes
    # first to a midi message, and remove it from its list.
    while noteOn.__len__() > 0 or noteOff.__len__() > 0:
        if noteOff.__len__() == 0 or (noteOn.__len__() > 0 and noteOn[0][1] < noteOff[0][1]):
            n = noteOn[0][0]
            msgType = 'note_on'
            msgTime = noteOn[0][1]
            noteOn.remove(noteOn[0])
        else:
            n = noteOff[0][0]
            msgType = 'note_off'
            msgTime = noteOff[0][1]
            noteOff.remove(noteOff[0])

        msgs.append(mido.Message(msgType, channel=0, note=n.pitch, velocity=n.velocity, time=msgTime - time))
        time = msgTime

    return msgs


