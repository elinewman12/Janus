from Song import Song
from Key import Key, Mode

# Create an empty song object
song = Song()

# Load the MIDI file into the song object
song.load(filename="../../MIDI Files/Gospel/John Newton/Amazing_Grace.mid")

print("Current song key: " + song.key.tonic + " " + song.key.mode)

detect_object = song.detect_key_by_phrase_endings()
print("detected key by phrase endings: " + detect_object[0].tonic + " " + detect_object[0].mode)

# Manually enter the key to change from/to
song.change_song_key(Key("B", Mode.MINOR), Key("B", Mode.LOCRIAN))

# Use the auto-detected key of the song
# song.change_song_key(song.key, Key("G", Mode.LOCRIAN))


song.save(filename="../../MIDI Files/Gospel/John Newton/Amazing_Grace_locrian.mid")
