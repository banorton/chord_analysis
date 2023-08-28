# TODO: Make a chord complexity system and make it so interpretation uses simplest complexity
# TODO: In chord analysis, determine 3 and 7 to get tonality, then determine addtitions, then determine alterations.

class Musical:
    LETTERS = ("", "C", "Db", "D", "Eb", "E", "F",
               "Gb", "G", "Ab", "A", "Bb", "B")
    RELNUMS = {"C": 1, "Db": 2, "D": 3, "Eb": 4, "E": 5, "F": 6,
               "Gb": 7, "G": 8, "Ab": 9, "A": 10, "Bb": 11, "B": 12}
    ROOTNUMS = ("", "1", "b9", "2", "b3", "3", "4",
                "b5", "5", "b6", "6", "b7", "7")

    def name_split(self, name):
        letter = name.rstrip('0123456789')
        octave = name[len(letter):]
        return letter, int(octave)

    def get_name(self, num):
        return str(self.LETTERS[num % 100]) + str(num // 100)

    def get_num(self, name):
        letter, octave = self.name_split(name)
        return int(octave * 100) + int(self.RELNUMS[letter])

    def get_relnum(self, letter, root='C'):
        if root == 'C':
            return self.RELNUMS[letter]
        else:
            shift_num = 13 - self.RELNUMS[root]
            if self.RELNUMS[letter] + shift_num > 12:
                return (self.RELNUMS[letter] + shift_num) % 13 + 1
            else:
                return self.RELNUMS[letter] + shift_num

    def get_letter(self, relnum):
        return self.LETTERS[relnum]

    def letters_to_rootnums(self, letters, root):
        self.root = root
        rootnums = []
        for letter in letters:
            try:
                rootnum = self.ROOTNUMS[self.get_relnum(letter, root)]
            except:
                print()
            rootnums.append(rootnum)
        return rootnums


class Key(Musical):
    def __init__(self, num):
        self.num = num
        self.name = None
        self.relnum = None
        self.letter = None
        self.octave = None
        self._build_key()

    def _build_key(self):
        self.relnum = self.num % 100
        self.letter = self.LETTERS[self.relnum]
        self.octave = self.num//100
        self.name = self.letter + str(self.octave)


class Piano(Musical):
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


class Chord(Musical):
    def __init__(self, notes, root="C"):
        self.type = None
        self.root = root
        self.name = ""
        if not notes:
            raise Exception('Chord must contain notes.')
        elif not isinstance(notes, str):
            raise Exception(
                'Input for the chord constructor must be a string (e.g. "1 b3 5 b7")')
        elif len(notes.split()) > 88:
            raise Exception('Too many notes.')
        elif any(map(str.isdigit, notes)):
            self.notes = notes.split()
            self.find_type(self.notes)
        else:
            letters = notes.split()
            self.notes = self.letters_to_rootnums(letters, letters[0])
            self.find_type(self.notes)
        try:
            self.name = self.root + self.type
        except:
            pass

    def find_type(self, notes):
        notes_set = set(notes)
        type_str = ""
        if set("1 3 5".split()).issubset(notes_set):
            # M7
            if "7" in notes_set:
                type_str = "M7"
            # dom7
            elif "b7" in notes_set:
                type_str = "7"
            # C6
            elif "6" in notes_set:
                type_str = "6"
            # M
            else:
                type_str = "M"
        elif set("1 b3 5".split()).issubset(notes_set):
            # m7
            if "b7" in notes_set:
                type_str = "M7"
            # dom7
            elif "7" in notes_set:
                type_str = "mM7"
            # m
            else:
                type_str = "m"
        elif set("1 b3 b5".split()).issubset(notes_set):
            # m7
            if "bb7" in notes_set or "6" in notes_set:
                type_str = "dim7"
            # dom7
            elif "b7" in notes_set:
                type_str = "m7b5"
            elif "7" in notes_set:
                type_str = "dimM7"
            # dim
            else:
                type_str = "dim"
        self.type = type_str


if __name__ == '__main__':
    chord = Chord("E Ab B Eb")
    print(chord.notes)
    print(chord.root)
    print(chord.type)
    print(chord.name)
