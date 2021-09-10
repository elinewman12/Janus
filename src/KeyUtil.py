
NOTES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
EQUIVALENCE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


# This method will shift all notes in the song up (positive numHalfSteps) or
# down (negative numHalfSteps) the number of half steps specified.
# (assuming there are no key changes)
#
# <jfwiddif>
def change_song_key_by_half_steps(song, num_half_steps):
    for track in song.tracks:
        for note in track.notes:
            note.pitch += num_half_steps
    return song


# This method will change the key of an entire song from an origin key to a destination key
# (assuming there are no key changes)
#
# <jfwiddif>
def change_song_key(song, origin_key, destination_key):
    origin_index = 0
    destination_index = 0
    offset = 0

    # Get the index of the origin key
    if origin_key in NOTES:
        origin_index = NOTES.index(origin_key)
    elif origin_key in EQUIVALENCE:
        origin_index = EQUIVALENCE.index(origin_key)
    else:
        raise SyntaxError("Origin Key needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")

    # Get the index of the destination key
    if destination_key in NOTES:
        destination_index = NOTES.index(destination_key)
    elif destination_key in EQUIVALENCE:
        destination_index = EQUIVALENCE.index(destination_key)
    else:
        raise SyntaxError("Destination Key needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")

    # discover offset (this is the number of half steps to move each note to get to the destination key)
    offset = destination_index - origin_index

    # apply the offset to each note
    for track in song.tracks:
        for note in track.notes:
            note.pitch += offset

    return song

# This method will change the key of a section of a song from an origin key to a destination key
# between the provided time intervals.  Time intervals are given in absolute
#
#
# <jfwiddif>
def change_key_for_interval(song, origin_key, destination_key, interval_begin, interval_end):
    origin_index = 0
    destination_index = 0
    offset = 0

    # Get the index of the origin key
    if origin_key in NOTES:
        origin_index = NOTES.index(origin_key)
    elif origin_key in EQUIVALENCE:
        origin_index = EQUIVALENCE.index(origin_key)
    else:
        raise SyntaxError("Origin Key needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")

    # Get the index of the destination key
    if destination_key in NOTES:
        destination_index = NOTES.index(destination_key)
    elif destination_key in EQUIVALENCE:
        destination_index = EQUIVALENCE.index(destination_key)
    else:
        raise SyntaxError("Destination Key needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")

    # discover offset (this is the number of half steps to move each note to get to the destination key)
    offset = destination_index - origin_index

    # apply the offset to each note within the time interval
    for track in song.tracks:
        for note in track.notes:
            if interval_begin <= note.time <= interval_end:
                note.pitch += offset
    return song
