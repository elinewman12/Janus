from Genre import Genre
from Song import Song
import os
from Key import Key


if __name__ == '__main__':

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
    # song.load(filename="../MIDI Files/Hip-Hop/Kanye West/24851_Gold-Digger.mid", print_file=True)

    # song.load(filename="../MIDI Files/Utility/C_Major_Pentatonic.mid", print_file=False)
    song.load(filename="../MIDI Files/Country/Garth Brooks/23224_Friends-in-Low-Places.mid", print_file=False)

    for track in song.tracks:
        print("track: " + track.track_name)
        for chord in track.chords:
            print("  Chord: ")
            for note in chord.notes:
                print("    " + str(note.pitch) + " Time: " + str(note.time) + " channel: " + str(note.channel))

    # print(song.to_string())

    # song.print_song()

    # song.load(filename="../MIDI Files/Hip-Hop/Kanye West/24851_Gold-Digger.mid", print_file=False)
    # song.get_note_frequency_graph("Gold Digger by Kanye West")
    # song.get_note_velocity_graph("Gold Digger by Kanye West")
    # song.load(filename="music samples/Mii Channel.mid", print_file=True)
    # song.load(filename="music samples/Megadeth-Symphony Of Destruction.mid", print_file=True)

    # print(song.to_string())

    # print(song.detect_key())

    # for track in song.tracks:
    #     print(track.track_name + " -- " + str(track.tag))

    # song.detect_key_by_phrase_endings()

    # song.change_song_key(origin_key=Key('F#', 'major'), destination_key=Key('C', 'major'))
    # song.save(filename="music samples/Megadeth-Tornado of Souls.mid", print_file=True)

    # song.save(filename="music samples/Mii Channel Output.mid", print_file=True)

