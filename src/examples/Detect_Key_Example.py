"""
    This is the example for how to use the key detection functionality in Song.  Feel free to edit the
    song which is loaded in on line #12 to try detecting keys/scales for other songs.
"""

from Song import Song

# Create an empty song object
song = Song()

# Load the MIDI file into the song object
song.load(filename="../../MIDI Files/Indie/Simon and Garfunkel/scarborough_fair.mid")

# Run the key detection algorithm and display it's findings
print(song.detect_key_and_scale())

# or alternatively song.detect_key returns the resulting keys/scales so if you don't care about the inner
# workings of the detection algorithm just print the result (or use it as a list) as such:
#
# print(detect_key)

