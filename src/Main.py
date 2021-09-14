from Song import Song


if __name__ == '__main__':
    song = Song()

    song.load(filename="music samples/Mii Channel.mid")

    song.tracks[1].instrument = 75    # 75 = Pan Flute

    song.save(filename="music samples/Mii Channel Output.mid", print_file=True)

    song.change_song_key(origin_key='F#', destination_key='F')

    song.save(filename="music samples/Mii Channel Key Change.mid")

