"""
    This is the example for how to use the note frequency graph functionality with Genres. It creates a bar graph
    of all the notes in a given genre and how many times they occur throughout.

"""

from Genre import Genre

# Create an empty song object
genre = Genre(type="Rock")

# Run the method to get the transition graph and view it
genre.get_notes_frequency_graph()
# The graph will be viewable in a pdf file in the file directory.