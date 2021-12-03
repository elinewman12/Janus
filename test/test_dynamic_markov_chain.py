import pytest
import FileIO as FileIO
from Control import Control
from Genre import Genre
from Note import Note
from Song import Song, SongLibrary
from Track import Track
from Key import Key, Mode
import mido
from dynamic_markov_chain import DynamicMarkovChain, chainType


def test_constructor():
    chord_chain = DynamicMarkovChain("chord chain", token_length=3, chain_type=chainType.CHORD)
    assert chord_chain.name == "chord chain"
    assert chord_chain.chain_type == chainType.CHORD
    assert chord_chain.token_length == 3
    note_chain = DynamicMarkovChain("note chain", token_length=4, chain_type=chainType.NOTE)
    assert note_chain.chain_type == chainType.NOTE


def test_add_song():
    chord_song = Song()
    note_song = Song()
    chord_song.load(filename="test MIDI/C_major_chords.mid")
    note_song.load(filename="test MIDI/C_major_scale.mid")
    chord_chain = DynamicMarkovChain("chord chain", token_length=1, chain_type=chainType.CHORD)
    chord_chain.add_song(chord_song)
    assert "0 4 7" in chord_chain.probabilities.keys()
    assert "0 4 7 11" in chord_chain.probabilities.keys()
    assert "0 4 7 11" in chord_chain.probabilities.get("0 4 7")[0]
    note_chain = DynamicMarkovChain("note chain", token_length=1, chain_type=chainType.NOTE)
    note_chain.add_song(note_song)
    assert "0" in note_chain.probabilities.keys()
    assert "2" in note_chain.probabilities.keys()
    assert 2 in note_chain.probabilities.get("0")[0]


def test_generate_pattern():
    chord_song = Song()
    note_song = Song()
    chord_song.load(filename="test MIDI/C_major_chords.mid")
    note_song.load(filename="test MIDI/C_major_scale.mid")

    # Create a chord and note markov chain with the given attributes
    chord_chain = DynamicMarkovChain("chord chain", token_length=1, chain_type=chainType.CHORD)
    note_chain = DynamicMarkovChain("note chain", token_length=1, chain_type=chainType.NOTE)

    # Train the new markov chains with the desired song
    chord_chain.add_song(chord_song)
    note_chain.add_song(note_song)

    # Create a new song to write to
    chord_output = Song()

    # Create a chord and melody track
    chords = chord_chain.generate_pattern(chord_output, num_notes=16, instrument=24, octave=4)

    # Add the generated tracks to a new song
    chord_output.add_track(chords)

    # Save the new written song
    #Here we need to manually test that this song has the C scale and C Chords in it
    chord_output.save(filename='test MIDI/chord_output.mid')
    note_output = Song()
    melody = note_chain.generate_pattern(note_output, num_notes=64, instrument=32, octave=5)
    note_output.add_track(melody)
    note_output.save(filename='test MIDI/note_output.mid')
