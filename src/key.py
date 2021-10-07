KEYS = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
EQUIVALENT_KEYS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

'''
    This class is how we are representing the key of a musical piece.  It consists of a simple data field (key)
    which is a string representation of the key such as 'C#', 'Db', 'F', etc.
'''


class Key:

    def __init__(self, key='C'):
        """ Constructor for the Key class.

        Args:
            key (str): Value for the key of the song. Defaults to 'C'.

        Raises:
            SyntaxError: If the key is not within the list of keys and their equivalents
        """        
        if key not in KEYS and key not in EQUIVALENT_KEYS:
            raise SyntaxError("Key '" + str(key) +
                              "' needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")
        else:
            self.key = key

    # Takes a key (as a string) and converts it to the index of this key based on the NOTES and EQUIVALENCE arrays
    # specified at the top of this file 
    def get_c_based_index_of_key(self):
        """ Takes a key (as a string) and converts it to the index of this key based on the NOTES and EQUIVALENCE
        arrays specified at the top of this file

        Raises:
            SyntaxError: The key is not a valid key within the list of keys and equivalents

        Returns:
            int: index of this key in the list of notes
        """ 
        if self.key in KEYS:
            index = KEYS.index(self.key)
        elif self.key in EQUIVALENT_KEYS:
            index = EQUIVALENT_KEYS.index(self.key)
        else:
            raise SyntaxError("Key '" + str(self.key) +
                              "' needs to be the key and #/b if necessary. Examples: 'C#', 'Db', 'F' etc")
        return index

