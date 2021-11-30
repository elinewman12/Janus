# Local workspace config, do not commit
import sys
sys.path.insert(1, '/Users/erinlitty/Desktop/CSC492/2021FallTeam17-DeHaan/src')

from Song import Song, SongLibrary
from Key import Key

song = Song()
song.load(filename=SongLibrary.BILLIE_EILISH_NO_TIME_TO_DIE, print_file=True)

print(song.key.tonic + " " + song.key.mode)
# song.change_song_key(origin_key=song.key, destination_key=Key('F', 'major'))
song.save("3. no_time_to_die.mid")