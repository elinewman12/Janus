import pytest
import FileIO
from Control import Control
from Note import Note
from Song import Song
from Track import Track
from Key import Key
import mido


def test_chord_functionality():
    """
        Tests the functionality of a chord object being properly ingested

        Tests using chords in a c-key
    """
    orig = Song()

    orig.load(filename="test MIDI/C_major_chord_single.mid")
    assert orig.tracks[1].chords[0].notes[0].pitch == 48  # The pitch of a C3 note
    assert orig.tracks[1].chords[0].notes[1].pitch == 52  # The pitch of a E3 note
    assert orig.tracks[1].chords[0].notes[2].pitch == 55  # The pitch of a G3 note


def test_chord_names():
    orig = Song()
    orig.load(filename="test MIDI/C_major_chords.mid")

    assert orig.tracks[1].chords[0].name == "C Major"
    assert orig.tracks[1].chords[1].name == "C Major Seventh"
    assert orig.tracks[1].chords[2].name == "D Minor"
    assert orig.tracks[1].chords[3].name == "D Minor Seventh"

def test_to_string():
    orig = Song()

    orig.load(filename="test MIDI/C_major_chord_single.mid")
    test_string = orig.tracks[1].chords[0].to_string()
    assert test_string == "0 4 7"


def test_duplicate_chord():
    orig = Song()
    orig.load(filename="test MIDI/C_major_chord_single.mid")
    duplicate = orig.tracks[1].chords[0].duplicate_chord()
    assert duplicate.notes[0].pitch == orig.tracks[1].chords[0].notes[0].pitch
    assert duplicate.notes[1].pitch == orig.tracks[1].chords[0].notes[1].pitch
    assert duplicate.notes[2].pitch == orig.tracks[1].chords[0].notes[2].pitch