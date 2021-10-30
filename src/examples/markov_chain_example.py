import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/Users/erinlitty/Desktop/CSC492/2021FallTeam17-DeHaan/src')

from markov_chain import MarkovChain, Type
from markov_library import MarkovLibrary
from Song import Song

# Create an empty song object
song = Song()

# Load the MIDI file into the song object
# song.load(filename="MIDI Files/Metal/Megadeth/Megadeth-Symphony Of Destruction.mid")
song.load(filename="MIDI Files/Rock/Greenday/BoulevardofBrokenDreams.mid")

chain = MarkovChain("test chain", Type.NOTE_TONE)
chain.add_track(song.tracks[5])

lib = MarkovLibrary()
lib.add_markov_chain(chain)

song2 = Song()
lib.generate_pattern(song=song2, num_notes=50, note_tone_chain=lib.chains["test chain"])
song2.save('generated_song.mid', True)
