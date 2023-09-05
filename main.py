import pygame.midi as pgm


class Chord_Name:
    def __init__(
        self,
        type="",
        extensions="",
        slash="",
        suspensions="",
        additions=[],
        alterations=[],
    ):
        self.type = type
        self.extensions = extensions
        self.slash = slash
        self.suspensions = suspensions
        self.additions = additions
        self.alterations = alterations


class Musical:
    LETTERS = ("", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")
    RELNUMS = {
        "C": 1,
        "C#": 2,
        "Db": 2,
        "D": 3,
        "D#": 4,
        "Eb": 4,
        "E": 5,
        "F": 6,
        "F#": 6,
        "Gb": 7,
        "G": 8,
        "G#": 9,
        "Ab": 9,
        "A": 10,
        "A#": 9,
        "Bb": 11,
        "B": 12,
    }
    ROOTNUMS = ("", "1", "b2", "2", "b3", "3", "4", "b5", "5", "b6", "6", "b7", "7")

    def name_split(self, name):
        letter = name.rstrip("0123456789")
        octave = name[len(letter) :]
        return letter, int(octave)

    def get_name(self, num):
        return str(self.LETTERS[num % 100]) + str(num // 100)

    def get_num(self, name):
        letter, octave = self.name_split(name)
        return int(octave * 100) + int(self.RELNUMS[letter])

    def get_relnum(self, letter, root="C"):
        if root == "C":
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
        return rootnums


class Chord(Musical):
    def __init__(self, notes, root="C"):
        self.type = None
        self.root = root
        self.names = []
        if not notes:
            raise Exception("Chord must contain notes.")
        elif not isinstance(notes, str):
            raise Exception(
                'Input for the chord constructor must be a string (e.g. "1 b3 5 b7")'
            )
        elif len(notes.split()) > 88:
            raise Exception("Too many notes.")
        elif any(map(str.isdigit, notes)):
            self.notes = notes.split()
            self.type = self.find_name(self.notes)
            self.names = self.find_names(self.notes)
        else:
            letters = notes.split()
            self.notes = self.letters_to_rootnums(letters, letters[0])
            self.type = self.find_name(self.notes)
            self.names = self.find_names(letters)

    def find_names(self, notes):
        self.root = notes[0]
        chords = []
        roots = notes.copy()
        for root in roots:
            chord = self.letters_to_rootnums(notes, root)
            chords.append(chord)

        names = []
        for i, chord in enumerate(chords):
            name = self.find_name(chord)
            if i != 0:
                name.slash = "/" + str(self.root)

            if name.alterations:
                name_str = (
                    roots[i]
                    + name.type
                    + name.extensions
                    + name.slash
                    + "("
                    + "".join(name.alterations)
                    + ")"
                )
            else:
                name_str = roots[i] + name.type + name.extensions + name.slash
            names.append(name_str)
        return names

    def find_name(self, notes):
        try:
            notes_set = set(notes)
        except:
            raise Exception("Notes not valid.")
        if len(notes_set) == 1:
            return Chord_Name(type=notes[0])

        name = Chord_Name()

        # 7th chords
        if ("7" in self.notes) or ("b7" in self.notes):
            if "7" in self.notes:
                if "3" in self.notes:
                    name.type = "maj"
                    name.extensions = "7"
                elif "b3" in self.notes:
                    name.type = "mM"
                    name.extensions = "7"
                else:
                    if ("2" in self.notes) and not ("4" in self.notes):
                        name.suspensions = "sus2"
                    elif ("4" in self.notes) and not ("2" in self.notes):
                        name.suspensions = "sus4"
                    else:
                        name.suspensions = "sus"
            elif "b7" in self.notes:
                if "3" in self.notes:
                    name.type = "dom"
                    name.extensions = "7"
                elif "b3" in self.notes:
                    name.type = "min"
                    name.extensions = "7"
                    if "b5" in self.notes:
                        name.type = "min"
                        name.extensions = "7"
                        name.alterations = ["b5"]

            if "9" in self.notes:
                if "11" in self.notes:
                    if "13" in self.notes:
                        name.extensions = "13"
                    else:
                        name.extensions = "11"
                name.extensions = "9"

        # Not 7th chords
        else:
            if "b3" in self.notes:
                name.type = "min"
                if "b5" in self.notes:
                    name.type = "dim"
                    if "6" in self.notes:
                        name.type = "dim"
                        name.extensions = "7"
                        if "9" in self.notes:
                            if "11" in self.notes:
                                if "13" in self.notes:
                                    name.extensions = "13"
                                else:
                                    name.extensions = "11"
                            name.extensions = "9"
            elif "3" in notes_set:
                name.type = "maj"
                if "#5" in notes_set:
                    name.type = "aug"
            else:
                if ("2" in self.notes) and not ("4" in self.notes):
                    name.suspensions = "sus2"
                elif ("4" in self.notes) and not ("2" in self.notes):
                    name.suspensions = "sus4"
                else:
                    name.suspensions = "sus"

        for note in "1 2 b3 3 4 5 #5 6 b7 7 9 11 13".split():
            notes_set.discard(note)

        name.alterations = list(notes_set)
        return name


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
        self.octave = self.num // 100
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


if __name__ == "__main__":
    chord = Chord("C Eb G Bb")
    print(chord.notes)
    print(chord.root)
    print(chord.type)
    print(chord.names)
