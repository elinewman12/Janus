import FileIO


if __name__ == '__main__':
    song = FileIO.read_midi_file("music samples/Mii Channel.mid")

    for note in song.tracks[1].notes[:30]:
        print(str(note.pitch) + ' ' + str(note.duration))
