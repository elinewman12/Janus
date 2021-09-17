from Song import Song


if __name__ == '__main__':
    song = Song()

    # song.load(filename="../MIDI Files/Metal/Megadeth/Megadeth-Symphony Of Destruction.mid")
    song.load(filename="music samples/Megadeth-Symphony Of Destruction.mid", print_file=True)

    # song.tracks[1].instrument = 75    # 75 = Pan Flute
    # song.print_song()

    song.save(filename="music samples/Megadeth-Symphony Of Destruction 2.mid", print_file=True)

    # song.change_song_key(origin_key='F#', destination_key='F')

    # song.save(filename="music samples/Mii Channel Key Change.mid")

