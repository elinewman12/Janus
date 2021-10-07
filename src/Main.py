from Genre import Genre
from Song import Song
import os
from Key import Key


if __name__ == '__main__':

    # genre = Genre(name="EDM")
    # directory = r'C:\Users\eliis\OneDrive\Documents\GitHub\2021FallTeam17-DeHaan\MIDI Files' + '\\' + genre.name
    # for artist in os.listdir(directory):
    #     artist_directory = directory + '\\' + artist.title()
    #     for song in os.listdir(artist_directory):
    #         song_object = Song()
    #         print(song)
    #         try:
    #             song_object.load(filename=artist_directory + '\\' + song.title())
    #         except (IOError, AttributeError) as e:
    #             continue
    #
    #         genre.add_song(song_object)
    #
    # genre.get_notes_frequency_graph()
    # genre.print_songs()

    song = Song()

    song.load(filename="../MIDI Files/Hip-Hop/Kanye West/24851_Gold-Digger.mid", print_file=False)
    # song.get_note_frequency_graph("Gold Digger by Kanye West")
    song.get_note_velocity_graph("Gold Digger by Kanye West")
    # song.load(filename="music samples/Mii Channel.mid", print_file=True)
    # song.load(filename="music samples/Megadeth-Symphony Of Destruction.mid", print_file=True)

    # song.tracks[1].instrument = 75    # 75 = Pan Flute
    # print(song.to_string())

    # print(song.detect_key())

    # song.change_song_key(origin_key=Key('F#'), destination_key=Key('C'))
    # song.save(filename="music samples/Megadeth-Tornado of Souls.mid", print_file=True)

    # song.save(filename="music samples/Mii Channel Output.mid", print_file=True)

