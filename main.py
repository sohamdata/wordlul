import cmd2
import os
import sys
from pathlib import Path


def popularity(word):
    freqs = {
        'a': 0.109162760775664, 'b': 0.026651962135833103, 'c': 0.03547468063597096,
        'd': 0.03424317617866005, 'e': 0.0972888521275618, 'f': 0.014851576141898722,
        'g': 0.024703611800385994, 'h': 0.030364856171307783, 'i': 0.06363385718224428,
        'j': 0.004484881904236743, 'k': 0.022277364212848084, 'l': 0.054333241430015625,
        'm': 0.03172502527341237, 'n': 0.052678981711239775, 'o': 0.06523297491039426,
        'p': 0.029335539012958368, 'q': 0.0018013050271114787, 'r': 0.06786140979689367,
        's': 0.06716294458229942, 't': 0.05288116901020127, 'u': 0.043819501884018015,
        'v': 0.010587262200165426, 'w': 0.014998621450234353, 'x': 0.004742211193824097,
        'y': 0.033893943571362925, 'z': 0.0058082896792574215
    }

    word = set(word)
    ret = 0
    for c in word:
        ret += freqs[c]
    return ret


class Wordle(cmd2.Cmd):
    """Wordle helper!"""

    def _initialize(self):
        if not hasattr(self, 'initial_words'):
            with open(self.dictionary_filename, 'r') as f:
                self.initial_words = set(f.read().lower().split())
                self.initial_words = list(
                    filter(lambda x: len(x) == 5, self.initial_words))
                self.initial_words.sort(key=popularity, reverse=True)
        self.words = self.initial_words[::]
        self.prev_words = []

        if (os.name == 'posix'):
            os.system('clear')
        else:
            os.system('cls')

    def __init__(self, dictionary_filename):
        super().__init__()
        self.hidden_commands.append('alias')
        self.hidden_commands.append('edit')
        self.hidden_commands.append('help')
        self.hidden_commands.append('history')
        self.hidden_commands.append('ipy')
        self.hidden_commands.append('macro')
        self.hidden_commands.append('py')
        self.hidden_commands.append('run_pyscript')
        self.hidden_commands.append('run_script')
        self.hidden_commands.append('set')
        self.hidden_commands.append('shell')
        self.hidden_commands.append('shortcuts')
        self.prompt = 'WORDLE HELPER > '

        self.dictionary_filename = dictionary_filename
        self._initialize()

    def print_cur_words(self):
        if not self.words:
            print("No words left!")
            return
        print(f'{len(self.words)} WORDS: {", ".join(self.words[:20])}', end='')
        if len(self.words) > 20:
            print(', etc...')
        else:
            print('')

    def do_reset(self, _line):
        """
        Reset to include all words
        """
        self._initialize()

    def do_words(self, _line):
        """
        Print current words
        """
        self.print_cur_words()

    def do_rm(self, line):
        """
        rm <letters>

        Removes all words that include given letters.
        E.g. [rm abcdef]
        """
        line = line.lower()
        if not line.isalpha():
            self.do_help('rm')
            return
        self.prev_words.append(self.words[::])
        self.words = list(filter(lambda x: len(
            set(line).intersection(x)) == 0, self.words))
        self.print_cur_words()

    def do_at(self, line):
        """
        at <index> <letter>

        Remove all words that don't have <letter> at <index>.
        <index> is in [1, 5]
        E.g. [at 1 a]
        """
        line = line.lower()
        line = line.split()
        if len(line) != 2 or not line[0].isdigit() or len(line[1]) != 1 or not line[1].isalpha():
            self.do_help('at')
            return
        i = int(line[0])
        if i < 1 or i > 5:
            self.do_help('at')
            return
        self.prev_words.append(self.words[::])
        self.words = list(filter(lambda x: x[i-1] == line[1], self.words))
        self.print_cur_words()

    def do_not(self, line):
        """
        not <index> <letter>

        Remove all words that have <letter> at <index>, as well as all word that don't have <letter> at all.
        <index> is in [1, 5]
        E.g. [at 1 a]
        """
        line = line.lower()
        line = line.split()
        if len(line) != 2 or not line[0].isdigit() or len(line[1]) != 1 or not line[1].isalpha():
            self.do_help('not')
            return
        i = int(line[0])
        if i < 1 or i > 5:
            self.do_help('not')
            return
        self.prev_words.append(self.words[::])
        self.words = list(
            filter(lambda x: x[i-1] != line[1] and line[1] in x, self.words))
        self.print_cur_words()

    def do_undo(self, _line):
        """
        Undo previous refinement (rm, at, not)
        """
        if not self.prev_words:
            print('No further undo')
            return
        self.words = self.prev_words.pop()
        self.print_cur_words()


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    c = Wordle(f'{script_dir}/words.txt')
    sys.exit(c.cmdloop())


if __name__ == '__main__':
    main()
