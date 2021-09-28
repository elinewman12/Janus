from Song import Song
from Key import Key


if __name__ == '__main__':
    song = Song()

    # song.load(filename="../MIDI Files/Hip-Hop/Kanye West/24851_Gold-Digger.mid", print_file=True)
    song.load(filename="../MIDI Files/Utility/C_Major_Pentatonic.mid", print_file=False)
    # song.load(filename="music samples/Megadeth-Symphony Of Destruction.mid", print_file=True)

    # song.tracks[1].instrument = 75    # 75 = Pan Flute
    # song.print_song()
    print(song.detect_key())

    # song.change_song_key(origin_key=Key('F#'), destination_key=Key('C'))
    # song.save(filename="music samples/Megadeth-Tornado of Souls.mid", print_file=True)


    # song.save(filename="music samples/Mii Channel Output.mid", print_file=True)

