# Local workspace config, do not commit
import sys
sys.path.insert(1, '/Users/erinlitty/Desktop/CSC492/2021FallTeam17-DeHaan/src')

from Song import Song, SongLibrary
from dynamic_markov_chain import DynamicMarkovChain, chainType
from Rhythm import *
from Note import MAX_VELOCITY

song = Song()
song2 = Song()
song.load(filename=SongLibrary.IMAGINE_DRAGONS_RADIOACTIVE, print_file=False)
chord_chain = DynamicMarkovChain("chord chain", token_length=10, chain_type=chainType.CHORD)
chord_chain.add_song(song)
song2.add_track(chord_chain.generate_pattern(song2, num_notes=17, instrument=52, arpeggio=False, velocity=int(MAX_VELOCITY/2), octave=3))

note_chain = DynamicMarkovChain("note chain", token_length=10, chain_type=chainType.NOTE)
note_chain.add_song(song)
rhythm_1 = note_chain.generate_pattern(song2, num_notes=15, instrument=46, channel=2, velocity=int(MAX_VELOCITY), octave=4)
Rhythm.apply_rhythm_pattern(song=song2, track=rhythm_1, pattern_array=[EIGHTH, EIGHTH, EIGHTH, DOTTED_QUARTER, DOTTED_QUARTER])
song2.add_track(rhythm_1)
bridge_1 = note_chain.generate_pattern(song2, num_notes=10, instrument=46, channel=2, velocity=int(MAX_VELOCITY), octave=4)
song2.append_track(1, bridge_1)
song2.append_track(1, rhythm_1)
bridge_2 = note_chain.generate_pattern(song2, num_notes=10, instrument=46, channel=2, velocity=int(MAX_VELOCITY), octave=4)
song.append_track(1, bridge_2)
song.append_track(1, rhythm_1)
song.append_track(1, rhythm_1)
song2.save('generated_song.mid', True)