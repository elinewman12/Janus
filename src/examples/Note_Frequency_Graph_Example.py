"""
    This is the example for how to use the note frequency graph functionality. It creates a bar graph
    of all the notes in a song and how many times they occur throughout. You are also able to use this
    feature with multiple songs, so you can analyze a genre or an artist.

"""

from Song import Song

# Create an empty song object
song = Song()

# Load the MIDI file into the song object
song.load(filename="../../MIDI Files/Rock/Elton John/RocketMan.mid")

# Run the method to get the transition graph and view it
song.get_note_frequency_graph("Rocket Man")
# The graph will be viewable in a pdf file in the file directory.