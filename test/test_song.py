import pytest
import file_io as FileIO
from control import Control
from note import Note
from song import Song
from track import Track
from key import Key
import mido


def test_song_constructor():
    """
        Tests the constructor of Song
    """    
    tracks = [Track()]

    song = Song()
    assert song.ticks_per_beat == 48
    assert len(song.tracks) == 0
    song = Song(ticks_per_beat=2)
    assert song.ticks_per_beat == 2
    song = Song(tracks=tracks, ticks_per_beat=3)
    assert song.tracks[0] == tracks[0]
    with pytest.raises(ValueError):
        song = Song(ticks_per_beat=-1)


def test_change_song_key_by_half_steps():
    """
        Tests the functionality of changing song key by a
        given number of half steps

        Tests using a C scale changed to a D scale
    """
    orig = Song()
    new_song = Song()
    d_scale = Song()

    orig.load(filename="test/test MIDI/C_major_scale.mid")
    orig = orig.change_song_key_by_half_steps(2)
    orig.save(filename="test/test MIDI/C_major_scale_Output.mid")

    new_song.load(filename="test/test MIDI/C_major_scale_Output.mid")
    d_scale.load(filename="test/test MIDI/D_major_scale.mid")

    assert new_song.tracks[1].notes[0].pitch == d_scale.tracks[1].notes[0].pitch
    assert new_song.tracks[1].notes[1].pitch == d_scale.tracks[1].notes[1].pitch
    assert new_song.tracks[1].notes[2].pitch == d_scale.tracks[1].notes[2].pitch
    assert new_song.tracks[1].notes[3].pitch == d_scale.tracks[1].notes[3].pitch


def test_change_song_key():
    """
        Tests the functionality of changing song key from one key to another
        Tests using a C scale changed to a D scale
    """
    orig = Song()
    new_song = Song()
    d_scale = Song()

    orig.load(filename="test/test MIDI/C_major_scale.mid")
    orig = orig.change_song_key(origin_key=Key('C'), destination_key=Key('D'))
    orig.save(filename="test/test MIDI/C_major_scale_Output.mid")

    new_song.load(filename="test/test MIDI/C_major_scale_Output.mid")
    d_scale.load(filename="test/test MIDI/D_major_scale.mid")

    assert new_song.tracks[1].notes[0].pitch == d_scale.tracks[1].notes[0].pitch
    assert new_song.tracks[1].notes[1].pitch == d_scale.tracks[1].notes[1].pitch
    assert new_song.tracks[1].notes[2].pitch == d_scale.tracks[1].notes[2].pitch
    assert new_song.tracks[1].notes[3].pitch == d_scale.tracks[1].notes[3].pitch


def test_change_key_for_interval():
    """
        Tests the functionality of changing song key for a certain interval

        Tests using a C scale changed to a D scale
    """
    orig = Song()
    new_song = Song()
    d_scale = Song()

    orig.load(filename="test/test MIDI/C_major_scale.mid")
    orig = orig.change_key_for_interval(origin_key=Key('C'), destination_key=Key('D'), interval_begin=0, interval_end=107)
    orig.save(filename="test/test MIDI/C_major_scale_Output.mid")

    new_song.load(filename="test/test MIDI/C_major_scale_Output.mid")
    d_scale.load(filename="test/test MIDI/D_major_scale.mid")

    assert new_song.tracks[1].notes[0].pitch == d_scale.tracks[1].notes[0].pitch


def test_equals():
    """
    Tests the equals method in Song that compares two song objects
    """
    song1 = Song(ticks_per_beat=100)   # Standard song
    song2 = Song(ticks_per_beat=100)   # Same as 1
    song3 = Song(ticks_per_beat=100)   # Different notes
    song4 = Song(ticks_per_beat=100)   # Different number of notes
    song5 = Song(ticks_per_beat=100)   # Different Control messages
    song6 = Song(ticks_per_beat=100)   # Different number of control messages
    song7 = Song(ticks_per_beat=100)   # Different track name
    song8 = Song(ticks_per_beat=100)   # Different track device
    song9 = Song(ticks_per_beat=100)   # Different number of tracks
    song10 = Song(ticks_per_beat=200)  # Different ticks_per_beat

    notes1 = []  # Standard set of notes
    notes2 = []  # Different values inside the notes
    notes3 = []  # Different number of notes

    control1 = []  # Standard set of controls
    control2 = []  # Different values inside controls
    control3 = []  # Different number of controls

    notes1.append(Note(pitch=100, time=10, duration=10, velocity=50))
    notes1.append(Note(pitch=110, time=15, duration=15, velocity=55))

    notes2.append(Note(pitch=100, time=10, duration=10, velocity=50))
    notes2.append(Note(pitch=110, time=16, duration=15, velocity=55))

    notes3.append(Note(pitch=100, time=10, duration=10, velocity=50))
    notes3.append(Note(pitch=110, time=15, duration=15, velocity=55))
    notes3.append(Note(pitch=110, time=16, duration=15, velocity=55))

    control1.append(Control(msg_type="program_change", instrument=10, time=100))
    control1.append(Control(msg_type="set_tempo", tempo=500000, time=100))

    control2.append(Control(msg_type="program_change", instrument=10, time=100))
    control2.append(Control(msg_type="set_tempo", tempo=500500, time=100))

    control3.append(Control(msg_type="program_change", instrument=10, time=100))
    control3.append(Control(msg_type="set_tempo", tempo=500000, time=100))
    control3.append(Control(msg_type="control_change", control=100, value=10, time=100))

    song1.add_track(Track(track_name="track1", track_device="Device 1", channel=1, notes=notes1, controls=control1))
    song2.add_track(Track(track_name="track1", track_device="Device 1", channel=1, notes=notes1, controls=control1))
    song3.add_track(Track(track_name="track1", track_device="Device 1", channel=1, notes=notes2, controls=control1))
    song4.add_track(Track(track_name="track1", track_device="Device 1", channel=1, notes=notes3, controls=control1))
    song5.add_track(Track(track_name="track1", track_device="Device 1", channel=1, notes=notes1, controls=control2))
    song6.add_track(Track(track_name="track1", track_device="Device 1", channel=1, notes=notes1, controls=control3))
    song7.add_track(Track(track_name="track2", track_device="Device 1", channel=1, notes=notes1, controls=control1))
    song8.add_track(Track(track_name="track1", track_device="Device 2", channel=1, notes=notes1, controls=control1))
    song9.add_track(Track(track_name="track1", track_device="Device 1", channel=1, notes=notes1, controls=control1))
    song9.add_track(Track(track_name="track2", track_device="Device 2", channel=2, notes=notes1, controls=control1))
    song10.add_track(Track(track_name="track1", track_device="Device 1", channel=1, notes=notes1, controls=control1))

    assert song1.equals(song2)
    assert song1.equals(song3) is False
    assert song1.equals(song4) is False
    assert song1.equals(song5) is False
    assert song1.equals(song6) is False
    assert song1.equals(song7) is False
    assert song1.equals(song8) is False
    assert song1.equals(song9) is False
    assert song1.equals(song10) is False
    assert song2.equals(song1)
    assert song3.equals(song1) is False
    assert song4.equals(song1) is False
    assert song5.equals(song1) is False
    assert song6.equals(song1) is False
    assert song7.equals(song1) is False
    assert song8.equals(song1) is False
    assert song9.equals(song1) is False
    assert song10.equals(song1) is False

