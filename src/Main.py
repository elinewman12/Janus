from Song import Song


if __name__ == '__main__':
    song = Song()

    song.load(filename="music samples/Mii Channel.mid")

    song.save(filename="music samples/Mii Channel Output.mid")

