from markov_chain import MarkovChain
from Song import Song

# Create an empty song object
song = Song()

# Load the MIDI file into the song object
song.load(filename="MIDI Files/Metal/Megadeth/Medadeth-Symphony Of Destruction.mid")

chain = MarkovChain("test chain", 'note_tone')
print(chain.add_track(song.tracks[1]))
print("\n\n")
print(chain.add_track(song.tracks[2]))
