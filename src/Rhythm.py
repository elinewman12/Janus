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

        # print(song, track, pattern_array)
        # if pattern_array or song or track is None:
        #     raise SyntaxError("Needs a pattern_array, song and track")

        current_abs_time = 0
        whole_length = floor(song.ticks_per_beat * 4)
        for i, note in enumerate(track.notes):
            pattern_idx = i % len(pattern_array)
            # print(floor(pattern_array[pattern_idx] * whole_length))
            note.duration = floor(pattern_array[pattern_idx] * whole_length)
            # print(floor(current_abs_time))
            note.time = floor(current_abs_time)
            current_abs_time += note.duration