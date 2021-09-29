KEYS = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
EQUIVALENT_KEYS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


class Key:

    def __init__(self, key='C'):
        if key not in KEYS and key not in EQUIVALENT_KEYS:
            raise SyntaxError("Key '" + str(key) +
                              "' needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")
        else:
            self.key = key

    # Takes a key (as a string) and converts it to the index of this key based on the NOTES and EQUIVALENCE arrays
    # specified at the top of this file
    def get_c_based_index_of_key(self):
        if self.key in KEYS:
            index = KEYS.index(self.key)
        elif self.key in EQUIVALENT_KEYS:
            index = EQUIVALENT_KEYS.index(self.key)
        else:
            raise SyntaxError("Key '" + str(self.key) +
                              "' needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")
        return index
