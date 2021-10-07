KEYS = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
EQUIVALENT_KEYS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

'''
    This class is how we are representing the key of a musical piece.  It consists of a simple data field (key)
    which is a string representation of the key such as 'C#', 'Db', 'F', etc.
'''


class Key:

    def __init__(self, key='C'):
        if key not in KEYS and key not in EQUIVALENT_KEYS:
            raise SyntaxError("Key '" + str(key) +
                              "' needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")
        else:
            self.key = key

    def get_c_based_index_of_key(self):
        """ This will return the index of the key in the KEYS or equivalently in the EQUIVALENCE array.  This
        helps to understand the positioning of a key relative to C. It is useful for generating note frequencies
        consistently as well as knowing how to shift an array to be indexed at another Key

        :return: The index of the key relative to C.  For example 0 would be C, 1 would be C# or Db, 2 would be D etc.
        """
        if self.key in KEYS:
            index = KEYS.index(self.key)
        elif self.key in EQUIVALENT_KEYS:
            index = EQUIVALENT_KEYS.index(self.key)
        else:
            raise SyntaxError("Key '" + str(self.key) +
                              "' needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")
        return index

