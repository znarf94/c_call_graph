import os
import re
from collections import defaultdict
from os import walk
from pprint import pprint
from subprocess import call, Popen, PIPE

from typing import List, Dict, Optional

from cppcheckdata import parsedump, Token

CPP_CHECK = '/home/znarf/Téléchargements/cppcheck-1.82/cppcheck'


def main():
    function_calls = defaultdict(set)
    files_deps = defaultdict(set)
    func_decl_file = {}      # type: Dict[str, str]

    for dirpath, _, files in walk('.'):
        for basename in files:
            file = os.path.join(dirpath, basename)

            if file[-2:] == '.c':
                print(file)
                call([CPP_CHECK, '--dump', file])

                dump_file = file + '.dump'
                d = parsedump(dump_file)
                os.remove(dump_file)

                try:
                    # functions = d.configurations[0].functions
                    scopes = d.configurations[0].scopes
                    tokens = d.configurations[0].tokenlist  # type: List[Token]

                    for scope in scopes:
                        scope.tokens = [t for t in tokens if t.scopeId == scope.Id]

                    for scope in scopes:
                        if scope.type == 'Function':
                            func_decl_file[scope.function.name] = file
                            for t in scope.tokens:
                                if t.function is not None:
                                    function_calls[scope.function.name].add(t.function.name)

                except Exception as e:
                    print(e)

    # Dépendences entre fichiers .c
    for caller, callees in function_calls.items():
        for callee in callees:
            if caller in func_decl_file and callee in func_decl_file:
                files_deps[func_decl_file[caller]].add(func_decl_file[callee])

    pprint(function_calls, indent=2)
    pprint(func_decl_file, indent=2)
    pprint(files_deps, indent=2)

    dot_graph('calls', function_calls)
    dot_graph('files', files_deps)
    dot_graph('full', function_calls, reverse_dict(func_decl_file))


def reverse_dict(d):
    out = defaultdict(set)

    for k, v in d.items():
        out[v].add(k)

    return dict(out)


def dot_graph(name: str,
              d: Dict[str, str],
              clusters: Optional[Dict[str, str]] = None) -> None:
    dot = '''digraph d {
    rankdir = UD;
    node [shape = rectangle; style = rounded];
    '''

    if clusters is not None:
        r = re.compile('[~\W]')
        for cluster, nodes in clusters.items():
            dot += 'subgraph cluster_{} {{\n'.format(r.sub('_', cluster))
            dot += 'label = "{}"\n'.format(cluster)
            for node in sorted(nodes):
                dot += '"{}";\n'.format(node)
            dot += '}\n\n'

    for caller, callees in d.items():
        dot += '"{}" -> {{"{}"}};\n'.format(caller, '" "'.join(sorted(callees)))

    dot += '}'

    print('==================================================')
    print(dot)
    print('==================================================')

    outfile = name + '.png'
    p = Popen(['dot', '-Tpng', '-o', outfile], stdin=PIPE, stdout=PIPE)
    p.communicate(bytes(dot, 'utf8'))

    call(['xdg-open', outfile])


if __name__ == '__main__':
    main()
