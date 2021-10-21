from Song import Song

song = Song()

# song.load(filename="../../MIDI Files/Metal/Megadeth/Megadeth-Symphony Of Destruction.mid")    # Actual Key: E
# song.load(filename="../../MIDI Files/Rock/Aerosmith/DreamOn.mid")                             # Actual Key: F
# song.load(filename="../../MIDI Files/Country/John Anderson/2603_Seminole-Wind.mid")           # Actual Key: E
# song.load(filename="../../MIDI Files/Indie/Simon and Garfunkel/scarborough_fair.mid")         # Actual Key: E
# song.load(filename="../../MIDI Files/Rock/Elton John/RocketMan.mid")                          # Actual Key: Bb
song.load(filename="../../MIDI Files/Hip-Hop/Kanye West/21530_All-Falls-Down.mid")            # Actual Key: D#

print(song.detect_key_by_phrase_endings()[1])

# Prints a list of each track and its associated tag
# for track in song.tracks:
#     print(track.track_name + "  " + str(track.tag))
