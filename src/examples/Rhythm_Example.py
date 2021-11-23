from Rhythm import *
from Song import Song
from Track import TagEnum


song = Song()

# Load the MIDI file into the song object
song.load(filename="music samples/Mii Channel.mid")

# Rhythm pattern to apply to the song
pattern = [HALF, DOTTED_SIXTEENTH, EIGHTH, SIXTEENTH]

# Apply the rhythm pattern
Rhythm.apply_rhythm_pattern(song=song, track=song.tracks[1], pattern_array=pattern)

#save to midi file
song.save('rhythm.mid')