from Song import Song
from dynamic_markov_chain import DynamicMarkovChain, chainType

song = Song()
song.load(filename="../../MIDI Files/Rock/Greenday/GoodRiddance(TimeOfYourLife).mid")

chord_chain = DynamicMarkovChain("chord chain", token_length=3, chain_type=chainType.CHORD)
note_chain = DynamicMarkovChain("note chain", token_length=3, chain_type=chainType.NOTE)

song2 = Song()
chord_track1 = chord_chain.generate_pattern(song2, 8, 46)
melody_track1 = note_chain.generate_pattern(song2, 32, 25)

chord_track2 = chord_chain.generate_pattern(song2, 8, 46)
melody_track2 = note_chain.generate_pattern(song2, 32, 25)

chord_track = chord_track1.append_track(chord_track1)
melody_track = melody_track1.append_track(melody_track1)

chord_track = chord_track.append_track(chord_track2)
chord_track = chord_track.append_track(chord_track2)
melody_track = melody_track.append_track(melody_track2)
melody_track = melody_track.append_track(melody_track2)

song2.add_track(chord_track)
song2.add_track(melody_track)

song2.save(filename='../../MIDI Files/Generated/Structured Song.mid')