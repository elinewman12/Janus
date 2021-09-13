import sys

import mido
from mido import MidiFile
from Track import Track
from Note import Note


# Takes a song and file name as input, clears the song data and overwrites
# it with the data from the new file. This creates a list of tracks, gets
# the metadata for the song, and creates a "song" object
#
# <jmleeder>
def read_midi_file(song, file_name):
    midi = MidiFile(file_name)

    song.clear_song_data()
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
        raise NotImplementedError()

    # File has multiple synchronous tracks
    elif midi.type == 1:

        # For each mido track in the file
        for read_track in midi.tracks:

            # Make a new internal track representation
            track: Track = Track()
            # Notes that have had their note_on message read, but don't yet have a note_off message
            current_notes = []
            # The current running time of the song (In absolute terms)
            current_time = 0
            # For each message in the mido track
            for msg in read_track:

                # Add the delay between notes to the current time
                current_time += msg.time

                # If this message is a note and not metadata
                if hasattr(msg, 'note'):
                    handle_note(msg=msg, notes=current_notes, time=current_time, track=track)

            # Add this track and its associated notes to the song (sorted by time)
            track.notes.sort(key=lambda note: note.time)
            song.add_track(track)
        return song

    # File has multiple asynchronous tracks
    else:
        raise NotImplementedError()


# Takes a file name and a song as input,
# recreates a midi file using the tracks and metadata included
# in the song object, and exports it to a file with the given name
#
# <jmleeder>
def write_midi_file(song, file_name):
    # Generate new type 1 midi file with the original song's metadata
    midi = MidiFile(type=1)
    midi.ticks_per_beat = song.ticks_per_beat

    # For each track in the song
    for t in song.tracks:
        # Get an ordered list of messages
        msgs = order_messages(t)
        # Create a new midi track and add these messages to the track
        midi.add_track(name=None)
        for m in msgs:
            midi.tracks[len(midi.tracks) - 1].append(m)
    # Save this midi file
    midi.save(file_name)


# Takes a track as input and returns an ordered list of midi messages.
# These messages consist of note_on and note_off messages, and will
# have their attributes (channel, pitch, velocity, time) set correctly
# based on the values stored in each note object
#
# <jmleeder>
def order_messages(track):
    note_on = []
    note_off = []
    msgs = []
    time = 0

    # Generate two lists (note_on and note_off) that store the absolute
    # times when each note starts and ends. These lists consist of tuples,
    # [Note, int] that stores a note and it's corresponding time (either
    # starting or ending time)
    for n in track.notes:
        note_on.append([n, n.time])
        note_off.append([n, n.time + n.duration])

    # note_on will be sorted inside the track object, note_off may not be in the same order
    note_off.sort(key=lambda note: note[1])

    # Compare the first element of the note_on and note_off lists. Write which ever one comes
    # first to a midi message, and remove it from its list.
    while len(note_on) > 0 or len(note_off) > 0:
        if len(note_on) > 0:
            next_note_on = note_on[0][0]
            next_note_on_time = note_on[0][1]
        else:
            next_note_on = None
            next_note_on_time = None

        if len(note_off) > 0:
            next_note_off = note_off[0][0]
            next_note_off_time = note_off[0][1]
        else:
            next_note_off = None
            next_note_off_time = None

        if len(note_on) > 0 and next_note_on_time < next_note_off_time:
            n = next_note_on
            msgType = 'note_on'
            msgTime = next_note_on_time
            note_on.remove(note_on[0])
        else:
            n = next_note_off
            msgType = 'note_off'
            msgTime = next_note_off_time
            note_off.remove(note_off[0])

        msgs.append(mido.Message(type=msgType, channel=0, note=n.pitch, velocity=n.velocity, time=msgTime - time))
        time = msgTime

    return msgs


# Handles the case where a note message is read in from a midi file
# msg = the message being read in
# notes = A list of notes that have been started (note_on message) but not ended (no note_off message yet)
# time = the current timestamp where the previous note occurred
# track = the track this note will be added to
def handle_note(msg, notes, time, track):
    # If this message is the start of a note
    if msg.type == 'note_on':
        # Create a new Note object and add it to the array of currently playing notes
        notes.append(Note(pitch=msg.note, time=time, duration=0, velocity=msg.velocity))

    # If this message is the end of a note
    if msg.type == 'note_off':
        # For each note that is currently playing
        for n in notes:
            # Check if the pitch is the same (locate the correct note)
            if n.pitch == msg.note:
                # Set the duration of this note based on current_time - start time, add it to the track
                n.duration = time - n.time
                notes.remove(n)
                track.add_note(n)
                break
