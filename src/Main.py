from Genre import Genre
from Song import Song
import os

if __name__ == '__main__':
    genre = Genre(name="Rock")
    directory = r'C:\Users\Eli\Documents\GitHub\2021FallTeam17-DeHaan\MIDI Files' + '\\' + genre.name
    for artist in os.listdir(directory):
        artist_directory = directory + '\\' + artist.title()
        for song in os.listdir(artist_directory):
            song_object = Song()
            try:
                song_object.load(filename=artist_directory + '\\' + song.title())
            except NotImplementedError:
                continue

            genre.add_song(song_object)

    genre.get_notes_frequency_graph()
    genre.print_songs()

    song = Song()

    song.load(filename="music samples/Mii Channel.mid")

    song.get_note_frequency_graph()

    #song.change_song_key(origin_key='F#', destination_key='F')

    song.save(filename="music samples/Mii Channel Output.mid")

