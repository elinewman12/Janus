import collections

from Song import Song
from Track import Track
import FileIO
import matplotlib.pyplot as plt


class Genre:

    def __init__(self, songs=None, name=None):
        if songs is None:
            songs = []
        self.songs = songs
        self.name = name

    def add_song(self, song):
        assert isinstance(song, Song)
        self.songs.append(song)

    def print_songs(self):
        print(self.songs)

    def get_notes_frequency_graph(self):
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
