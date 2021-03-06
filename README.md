## Janus - Music Transformation
This project was created for the Senior Design Class CSC492 at North Carolina State University during the Fall 2021 semester. This project is sponsored by Mr. Michael DeHaan, an alumni of NC State. Janus allows users to transform, analyze, and generate music through many different features. Users can generate music using markov chains of various length, they can analyze existing songs through informative visualizations like chord transition graphs, and can also transform the mode, scale, or key of song.

## Tech/framework used
<b>Built with</b>
- [Python](https://www.python.org/)
- [Mido](https://mido.readthedocs.io/en/latest/)
- [Graphviz](https://graphviz.readthedocs.io/en/stable/manual.html)
- [Matplotlib](https://matplotlib.org/)

## Features
- Markov Chain:
  - Allows users to generate new music based on an existing library of songs. A user can input as many songs as they
    they would like to create a markov chain and then can generate a new song using a custom token length and instrument.
- Visualization:
  - Chord Transition Graph: Visualizes all of the chords present in a song and how often one chord follows another. 
    This can be useful to understand common chord progressions or patterns in the music of an artist or genre.
  - Chord/Note Frequency Graph: Visualizes the frequency of all the notes or chords occuring in a song or group of songs.
- Transformations:
  - Mode Change: Changes the mode of a song to a new given mode.

## Code Example
Show what the library does as concisely as possible, developers should be able to figure out **how** your project solves their problem by looking at the code example. Make sure the API you are showing off is obvious, and that your code is short and concise.

## Installation
Above your python script, import any of the Janus files. This will allow you to access all of our public methods.

## How to use?
First, import the project as described above.
Then, you may use any of the below features within your program:

- Markov Chain:
  - <code>DynamicMarkovChain(name,token_length)</code>
  - <code>add_song(song)</code>
  - <code>generate_pattern(chain,instrument,arpeggio)</code>
- Visualization:
  - <code>get_transition_graph(name)</code>
  - <code>get_notes_frequency_graph()</code>
  - <code>get_chord_frequency_graph()</code>
- Transformations:
  - <code>change_song_key()</code>

## Contribute

Feel free to continue contributing to this project. This is an open source repository so it is completely open for others to continue building on the work that our team has provided.

## Credits
This project was created by Eli Newman, Erin Litty, Nithika Aduri, James Leeder, and John Widdifield. Our sponsor is Michael DeHaan and the teaching staff is Margaret Heil and David Sturgill.
