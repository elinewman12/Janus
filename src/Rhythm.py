from Song import Song
from math import floor

QUARTER = 0.25
HALF = 0.5
TRIPLET = 0.3333
WHOLE = 1
EIGHTH = 0.1255
SIXTEENTH = 0.062775
DOTTED_QUARTER = 0.375
DOTTED_HALF = 0.75
DOTTED_WHOLE = 1.5
DOTTED_EIGHTH = EIGHTH + SIXTEENTH
DOTTED_SIXTEENTH = SIXTEENTH + SIXTEENTH/2


class Rhythm:

    def apply_rhythm_pattern(song=None, track=None, pattern_array=None):

        current_abs_time = track.notes[0].time
        whole_length = floor(song.ticks_per_beat * 4)
        previous_time = track.notes[0].time
        for i, note in enumerate(track.notes):
            if note.time is not previous_time:
                pattern_idx = i % len(pattern_array)

                note.duration = floor(pattern_array[pattern_idx] * whole_length)

                note.time = floor(current_abs_time)

                previous_time = current_abs_time

                current_abs_time += note.duration
            else:
                pattern_idx = i % len(pattern_array)
                note.duration = floor(pattern_array[pattern_idx] * whole_length)
                note.time = previous_time

