import os
from collections import defaultdict
from os import walk
from pprint import pprint
from subprocess import call, Popen, PIPE

from typing import List

from cppcheckdata import parsedump, Token

CPP_CHECK = '/home/znarf/Téléchargements/cppcheck-1.82/cppcheck'


def main():
    calls = defaultdict(set)
    for dirpath, _, files in walk('.'):
        for basename in files:
            file = os.path.join(dirpath, basename)

            if file[-2:] == '.c':
                print(file)
                call([CPP_CHECK, '--dump', file])

                dump_file = file + '.dump'
                d = parsedump(dump_file)
                os.remove(dump_file)

                # functions = d.configurations[0].functions
                # scopes = d.configurations[0].scopes
                tokens = d.configurations[0].tokenlist  # type: List[Token]

                for t in tokens:
                    if t.scope.function is not None:
                        if t.function is not None:
                            calls[t.scope.function.name].add(t.function.name)

                pprint(calls, indent=2)

    dot_graph(calls)


def dot_graph(d: defaultdict(set)) -> None:
    dot = 'digraph d {\n'

    for a, b in d.items():
        dot += '"{}" -> {{"{}"}};\n'.format(a, '" "'.join(b))

    dot += '}'

    outfile = "graph.png"
    p = Popen(['dot', '-Tpng', '-o', outfile], stdin=PIPE, stdout=PIPE)
    p.communicate(bytes(dot, 'utf8'))

    call(['xdg-open', outfile])


if __name__ == '__main__':
    main()
