import collections

from Song import Song
from Track import Track
import FileIO
import matplotlib.pyplot as plt


class Genre:

    def __init__(self, songs=None, name=None):
        """ Constructor for the Genre object

        Args:
            songs (Song[], optional): List of Songs in this genre. Defaults to None.
            name (String): Name of this genre. Defaults to None.
        """        
        if songs is None:
            songs = []
        self.songs = songs
        self.name = name

    def add_song(self, song):
        """ Adds a song to the genre's list of songs

        Args:
            song (Song): The song to add to the Genre
        """        
        assert isinstance(song, Song)
        self.songs.append(song)

    def print_songs(self):
        """ Prints the list of songs in this genre
        TODO: make this private
        """        
        print(self.songs)

    def get_notes_frequency_graph(self):
        """ Creates and displays the visualization of the frequency of each note within
        Songs of this genre.
        TODO: make this return rather than 'print'
        """        
        notes_list = Song.get_notes_array()
        all_notes = []
        for song in self.songs:
            for track in song.tracks:
                for note in track.notes:
                    all_notes.append(notes_list[note.pitch % 12])

        counter = collections.Counter(all_notes)
        counter = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
        plt.bar(x=counter.keys(), height=counter.values())
        plt.xlabel("Note")
        plt.ylabel("Frequency")
        # Change this to show title of song when that variable is available
        plt.title("Frequency of Notes in " + self.name)
        plt.show()
