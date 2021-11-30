from Song import Song
from Track import Track
from dynamic_markov_chain import DynamicMarkovChain, chainType

in_song = Song()
in_song.load(filename="../../MIDI Files/Grunge/Pearl Jam/Jeremy.mid")

chord_chain = DynamicMarkovChain("chord chain", token_length=3, chain_type=chainType.CHORD)
note_chain = DynamicMarkovChain("note chain", token_length=4, chain_type=chainType.NOTE)

chord_chain.add_song(in_song)
note_chain.add_song(in_song)

song2 = Song()
chd_verse = chord_chain.generate_pattern(song2, 4, 46, octave=4)
mel_verse = note_chain.generate_pattern(song2, 16, 72, octave=5)

chd_chorus = chord_chain.generate_pattern(song2, 4, 46, octave=4)
mel_chorus = note_chain.generate_pattern(song2, 8, 24, octave=5)
mel_chorus2 = note_chain.generate_pattern(song2, 8, 24, octave=5)

chord_track = Track(channel=1)
melody_track = Track(channel=0)

chord_track = chord_track.append_tracks([0, 0, 1, 1, 0, 0, 1, 1, 0, 0], [chd_verse, chd_chorus])
melody_track = melody_track.append_tracks([0, 0, 1, 1, 2, 1, 0, 0, 1, 2, 1, 2, 0, 0], [mel_verse, mel_chorus, mel_chorus2])

song2.add_track(chord_track)
song2.add_track(melody_track)

song2.save(filename='../../MIDI Files/Generated/Structured Song6.mid')