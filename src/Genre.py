import collections
import os
from Song import Song
from Track import Track
import FileIO as FileIO
import matplotlib.pyplot as plt


class Genre:

    def __init__(self, songs=None, type=None):
        """ Constructor for the Genre object

        Args:
            songs (Song[], optional): List of Songs in this genre. Defaults to None.
            name (String): Name of this genre. Defaults to None.
        """
        self.songs = []
        self.type = type
        directory = '..\\..\\MIDI Files\\' + type
        for artist in os.listdir(directory):
            artist_directory = directory + '\\' + artist.title()
            for song in os.listdir(artist_directory):
                song_object = Song()
                try:
                    song_object.load(filename=artist_directory + '\\' + song.title())
                except (IOError, AttributeError) as e:
                    continue
                assert isinstance(song_object, Song)
                self.songs.append(song_object)

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

        bar = song.get_bar_graph(title="Frequency of Notes in " + self.type,
                                 x_label="Note", y_label="Frequency", items=all_notes)
        plt.show()

