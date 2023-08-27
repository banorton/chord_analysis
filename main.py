class Key:
    _LETTERS = ("", "C", "Db", "D", "Eb", "E", "F",
                "Gb", "G", "Ab", "A", "Bb", "B")

    def __init__(self, num):
        self.num = num
        self.name = None
        self.relnum = None
        self.letter = None
        self.octave = None
        self._build_key()

    def _build_key(self):
        self.relnum = self.num % 100
        self.letter = self._LETTERS[self.relnum]
        self.octave = self.num//100
        self.name = self.letter + str(self.octave)


class Piano:
    _LETTERS = ("", "C", "Db", "D", "Eb", "E", "F",
                "Gb", "G", "Ab", "A", "Bb", "B")

    _RELNUMS = {"C": 1, "Db": 2, "D": 3, "Eb": 4, "E": 5, "F": 6,
                "Gb": 7, "G": 8, "Ab": 9, "A": 10, "Bb": 11, "B": 12}

    def __init__(self):
        self.keys = {}
        self._build_piano()

    def _build_piano(self):
        # Build the keys for a standard 88 key piano.
        # First, build the bottom 3 keys of a piano that are the only ones in their octave (A0, Bb0, and B).
        self.keys[10] = Key(10)
        self.keys[11] = Key(11)
        self.keys[12] = Key(12)

        # Build the keys in octaves 1 to 7.
        for octave in range(1, 8):
            for relnum in range(1, 13):
                num = (octave * 100) + relnum
                self.keys[num] = Key(num)

        # Build the highest key C8 which is also in an octave of its own.
        self.keys[801] = Key(801)

    def name_split(self, name):
        letter = name.rstrip('0123456789')
        octave = name[len(letter):]
        return letter, int(octave)

    def get_name(self, num):
        return str(self._LETTERS[num % 100]) + str(num // 100)

    def get_num(self, name):
        letter, octave = self.name_split(name)
        return int(octave * 100) + int(self._RELNUMS[letter])

    def get_relnum(self, letter):
        return self._RELNUMS[letter]

    def get_letter(self, relnum):
        return self._LETTERS[relnum]


if __name__ == '__main__':
    piano = Piano()
