from Song import Song
from dynamic_markov_chain import DynamicMarkovChain, chainType

song = Song()
song.load(filename="../../MIDI Files/Rock/Greenday/GoodRiddance(TimeOfYourLife).mid")

chord_chain = DynamicMarkovChain("chord chain", token_length=3, chain_type=chainType.CHORD)
note_chain = DynamicMarkovChain("note chain", token_length=3, chain_type=chainType.NOTE)

chord_chain.add_song(song)
note_chain.add_song(song)

song2 = Song()
chord_track_verse = chord_chain.generate_pattern(song2, 8, 46)
melody_track_verse = note_chain.generate_pattern(song2, 32, 25)

chord_track_chorus = chord_chain.generate_pattern(song2, 8, 46)
melody_track_chorus = note_chain.generate_pattern(song2, 32, 25)

chord_track = chord_track_verse.append_track(chord_track_verse)
melody_track = melody_track_verse.append_track(melody_track_verse)

chord_track = chord_track.append_track(chord_track_chorus)
chord_track = chord_track.append_track(chord_track_chorus)
melody_track = melody_track.append_track(melody_track_chorus)
melody_track = melody_track.append_track(melody_track_chorus)

song2.add_track(chord_track)
song2.add_track(melody_track)

song2.save(filename='../../MIDI Files/Generated/Structured Song.mid')