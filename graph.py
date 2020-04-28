from pprint import pprint

from pyparsing import *

if __name__ == '__main__':
    comment = Literal(';;') + restOfLine
    ident = Regex('@\d+')

    l_type = Word(alphas + '_')
    attr_value = Word(alphanums + '.:') | ident
    attr_name = Word(alphanums + '_ ').setParseAction(lambda toks: toks[0].strip())
    attr = Dict(Group(attr_name + Literal(':').suppress() + attr_value))
    attrs = Group(ZeroOrMore(attr))

    useful_line = Dict(Group(ident + Group(l_type + attrs)))
    line = comment.suppress() | useful_line
    file = ZeroOrMore(line)

    d = file.parseFile('main.c.003t.original')
    pprint(d.asDict(), indent=2)
