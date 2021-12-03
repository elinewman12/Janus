from Rhythm import *
from Song import Song, SongLibrary
from Track import TagEnum


song = Song()

# Load the MIDI file into the song object
song.load(filename=SongLibrary.AMAZING_GRACE)

# Rhythm pattern to apply to the song
pattern = [EIGHTH, SIXTEENTH, EIGHTH_TRIPLET, EIGHTH_TRIPLET, EIGHTH_TRIPLET, SIXTEENTH, QUARTER_REST, QUARTER]

# Apply the rhythm pattern
apply_rhythm_pattern(song=song, track=song.tracks[1], pattern_array=pattern)

# Adds human aspect to rhythm by slightly offsetting rhythm timings
humanify_rhythm(song=song, track=song.tracks[1], humanify_percent=0.3)

#save to midi file
song.save('../../MIDI Files/Demo Output/rhythm.mid')