from Song import Song, SongLibrary
from Key import Key, Mode

# Create an empty song object
song = Song()

# Load the MIDI file into the song object
song.load(filename=SongLibrary.SIMON_AND_GARFUNKEL_SOUND_OF_SILENCE)

# Manually enter the key to change from/to
song.change_song_key(Key("E", Mode.MINOR), Key("E", Mode.MAJOR))

# Use the auto-detected key of the song
# song.change_song_key(song.key, Key("G", Mode.MINOR))


song.save(filename="../../MIDI Files/Demo Output/Sound_Of_Silence_Major.mid")
