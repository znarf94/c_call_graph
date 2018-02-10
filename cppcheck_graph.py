from collections import defaultdict
from os import walk
from pprint import pprint
from subprocess import call
from typing import List

from cppcheckdata import parsedump, Token

CPP_CHECK = '/home/znarf/Téléchargements/cppcheck-1.82/cppcheck'

if __name__ == '__main__':
    calls = defaultdict(set)

    for _, _, files in walk('.'):
        for file in files:
            if file[-2:] == '.c':
                print(file)
                call([CPP_CHECK, '--dump', file])

                d = parsedump(file + '.dump')

                functions = d.configurations[0].functions
                scopes = d.configurations[0].scopes
                tokens = d.configurations[0].tokenlist  # type: List[Token]

                for t in tokens:
                    if t.scope.function is not None:
                        if t.function is not None:
                            calls[t.scope.function.name].add(t.function.name)

                pprint(calls, indent=2)
