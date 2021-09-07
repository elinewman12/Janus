import FileIO


if __name__ == '__main__':
    song = FileIO.read_midi_file("music samples/Mii Channel.mid")

    FileIO.write_midi_file("music samples/Mii Channel Output.mid", song)

