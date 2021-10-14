from Genre import Genre
from Song import Song
import os
from Key import Key


if __name__ == '__main__':
    # genre = Genre(name="Rock")
    # directory = r'C:\Users\Eli\Documents\GitHub\2021FallTeam17-DeHaan\MIDI Files' + '\\' + genre.name
    # for artist in os.listdir(directory):
    #     artist_directory = directory + '\\' + artist.title()
    #     for song in os.listdir(artist_directory):
    #         song_object = Song()
    #         try:
    #             song_object.load(filename=artist_directory + '\\' + song.title())
    #         except NotImplementedError:
    #             continue
    #
    #         genre.add_song(song_object)
    #
    # genre.get_notes_frequency_graph()
    # genre.print_songs()

    song = Song()
    song.load(filename="../MIDI Files/Rock/Elton John/CircleofLife.mid", print_file=True)
    # song.load(filename="../MIDI Files/Hip-Hop/Kanye West/24851_Gold-Digger.mid", print_file=True)
    # song.load(filename="music samples/Mii Channel.mid", print_file=True)
    # song.load(filename="music samples/Megadeth-Symphony Of Destruction.mid", print_file=False)

    # song.tracks[1].instrument = 75    # 75 = Pan Flute
    # song.print_song()
    # print(song.detect_key())

    # song.detect_key_by_phrase_endings()

    # song.change_song_key(origin_key=Key('F#'), destination_key=Key('C'))
    # song.save(filename="music samples/Megadeth-Tornado of Souls.mid", print_file=True)

    # song.save(filename="music samples/Mii Channel Output.mid", print_file=True)

