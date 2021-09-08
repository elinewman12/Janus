
NOTES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
EQUIVALENCE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# This method will shift all notes in the song up (positive numHalfSteps) or
# down (negative numHalfSteps) the number of half steps specified.
#(assuming there are no key changes)
#
# <jfwiddif>
def changeSongKeyByHalfSteps(song, numHalfSteps):
    for track in song.tracks:
        for note in track.notes:
            note.pitch += numHalfSteps
    return song

# This method will change the key of an entire song from an origin key to a destination key
# (assuming there are no key changes)
#
# <jfwiddif>
def changeSongKey(song, originKey, destinationKey):
    origin_index = 0
    destination_index = 0
    offset = 0

    # Get the index of the origin key
    if originKey in NOTES:
        origin_index = NOTES.index(originKey)
    elif originKey in EQUIVALENCE:
        origin_index = EQUIVALENCE.index(originKey)
    else:
        raise SyntaxError("Origin Key needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")

    # Get the index of the destination key
    if destinationKey in NOTES:
        destination_index = NOTES.index(destinationKey)
    elif destinationKey in EQUIVALENCE:
        destination_index = EQUIVALENCE.index(destinationKey)
    else:
        raise SyntaxError("Destination Key needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")

    # discover offset (this is the number of half steps to move each note to get to the destination key)
    offset = destination_index - origin_index

    #apply the offset to each note
    for track in song.tracks:
        for note in track.notes:
            note.pitch += offset

    return song

# This method will change the key of a section of a song from an origin key to a destination key
# between the provided time intervals.  Time intervals are given in absolute
#
#
# <jfwiddif>
def changeKeyForInterval(song, originKey, destinationKey, intervalBegin, intervalEnd):
    origin_index = 0
    destination_index = 0
    offset = 0

    # Get the index of the origin key
    if originKey in NOTES:
        origin_index = NOTES.index(originKey)
    elif originKey in EQUIVALENCE:
        origin_index = EQUIVALENCE.index(originKey)
    else:
        raise SyntaxError("Origin Key needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")

    # Get the index of the destination key
    if destinationKey in NOTES:
        destination_index = NOTES.index(destinationKey)
    elif destinationKey in EQUIVALENCE:
        destination_index = EQUIVALENCE.index(destinationKey)
    else:
        raise SyntaxError("Destination Key needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")

    # discover offset (this is the number of half steps to move each note to get to the destination key)
    offset = destination_index - origin_index

    # apply the offset to each note within the time interval
    for track in song.tracks:
        for note in track.notes:
            if intervalBegin <= note.time <= intervalEnd:
                note.pitch += offset
    return song
