from Genre import Genre
from Song import Song
import os
from Key import Key


if __name__ == '__main__':

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
    
    song.load(filename="../MIDI Files/Utility/C_Major_Pentatonic.mid", print_file=False)
    # song.load(filename="music samples/Megadeth-Symphony Of Destruction.mid", print_file=False)

    print(song.to_string())

    print(song.detect_key())
    
    # song.load(filename="music samples/Mii Channel.mid", print_file=True)

    # song.print_song()
    # print(song.detect_key())

    # song.change_song_key(origin_key=Key('F#', 'major'), destination_key=Key('C', 'major'))
    # song.save(filename="music samples/Megadeth-Tornado of Souls.mid", print_file=True)

    # song.save(filename="music samples/Mii Channel Output.mid", print_file=True)

