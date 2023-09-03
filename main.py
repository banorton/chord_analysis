class Musical:
    LETTERS = ("", "C", "Db", "D", "Eb", "E", "F",
               "Gb", "G", "Ab", "A", "Bb", "B")
    RELNUMS = {"C": 1, "Db": 2, "D": 3, "Eb": 4, "E": 5, "F": 6,
               "Gb": 7, "G": 8, "Ab": 9, "A": 10, "Bb": 11, "B": 12}
    ROOTNUMS = ("", "1", "b2", "2", "b3", "3", "4",
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
        has7 = False
        for letter in letters:
            rootnum = self.ROOTNUMS[self.get_relnum(letter, root)]
            if rootnum in {"7", "b7"}:
                has7 = True
            rootnums.append(rootnum)

        if has7:
            for i, rootnum in enumerate(rootnums):
                if rootnum == "2":
                    rootnums[i] = "9"
                if rootnum == "b2":
                    rootnums[i] = "b9"
                if rootnum == "4":
                    rootnums[i] = "11"
                if rootnum == "6":
                    rootnums[i] = "13"
                if rootnum == "b6":
                    rootnums[i] = "b13"
            print(rootnums)
        return rootnums


class Chord(Musical):
    def __init__(self, notes, root="C"):
        self.type = None
        self.root = root
        self.names = []
        if not notes:
            raise Exception('Chord must contain notes.')
        elif not isinstance(notes, str):
            raise Exception(
                'Input for the chord constructor must be a string (e.g. "1 b3 5 b7")')
        elif len(notes.split()) > 88:
            raise Exception('Too many notes.')
        elif any(map(str.isdigit, notes)):
            self.notes = notes.split()
            # self.names = self.find_names(self.notes)
            self.type = self.find_type(self.notes)
        else:
            letters = notes.split()
            self.notes = self.letters_to_rootnums(letters, letters[0])
            # self.names = self.find_names(letters)
            self.type = self.find_type(self.notes)

    def find_names(self, notes):
        rootnums = []
        for root in self.LETTERS[1:]:
            rootnum = self.letters_to_rootnums(notes, root)
            if "1" in set(rootnum):
                rootnums.append(rootnums)

        names = []
        for notes in rootnums:
            names.append(self.find_type(notes))
        return names

    def find_type(self, notes):
        try:
            notes_set = set(notes)
            print(notes)
        except:
            raise Exception("Notes not valid.")
        type = ""
        extensions = []

        # No7
        if not (("7" in notes_set) or ("b7" in notes_set)):
            # maj
            if set("1 3 5".split()).issubset(notes_set):
                type = "maj"
            # min
            elif set("1 b3 5".split()).issubset(notes_set):
                type = "min"
            # dim
            elif set("1 b3 b5".split()).issubset(notes_set) and not ("5" in notes_set) and not ("6" in notes_set):
                type = "dim"
            # dim
            elif set("1 b3 #11".split()).issubset(notes_set) and not ("5" in notes_set) and not ("6" in notes_set):
                type = "dim"
            # aug
            elif set("1 3 #5".split()).issubset(notes_set) and not ("5" in notes_set):
                type = "aug"
            # aug
            elif set("1 3 b6".split()).issubset(notes_set) and not ("5" in notes_set):
                type = "aug"
            # sus2
            elif set("1 2 5".split()).issubset(notes_set) and not ("3" in notes_set) and not ("b3" in notes_set):
                type = "sus2"
            # sus4
            elif set("1 4 5".split()).issubset(notes_set) and not ("3" in notes_set) and not ("b3" in notes_set):
                type = "sus4"

        # 7th chords
        else:
            # maj7
            if set("1 3 5 7".split()).issubset(notes_set):
                type = "maj7"
            # min7
            elif set("1 b3 5 b7".split()).issubset(notes_set):
                type = "min7"
            # dim7
            elif set("1 b3 b5 6".split()).issubset(notes_set):
                type = "dim7"
            # min7(b5)
            elif set("1 b3 b5 b7".split()).issubset(notes_set):
                type = "min7"
                extensions.append("b5")

            if "13" in notes_set:
                type = type[:-1] + "13"
            elif "11" in notes_set:
                type = type[:-1] + "11"
            elif "9" in notes_set:
                type = type[:-1] + "9"
        return [type, extensions]


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


if __name__ == '__main__':
    chord = Chord("B D C E G")
    print(chord.notes)
    print(chord.root)
    print(chord.type)
    print(chord.names)
    if chord.type[1]:
        print(chord.root + chord.type[0] + "(" + ''.join(chord.type[1]) + ")")
    else:
        print(chord.root + chord.type[0])
