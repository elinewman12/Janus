import pytest
import FileIO as FileIO
from Control import Control
from Genre import Genre
from Note import Note
from Song import Song, SongLibrary
from Track import Track
from Key import Key, Mode
import mido


def test_genre_constructor():
    """
        Tests the constructor of Genre
    """
    genre = Genre(type="Rock")
    assert genre.type == "Rock"
    assert len(genre.songs) == 6


def test_add_song():
    genre = Genre(type="Rock")
    song = Song()
    song.load(filename="../MIDI Files/Grunge/Nirvana/Lithium.mid")
    genre.add_song(song)
    assert song in genre.songs

def test_note_frequency_graph():
    genre = Genre(type="Rock")
    genre.get_notes_frequency_graph()
