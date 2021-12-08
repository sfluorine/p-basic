#!/usr/bin/env pypy3

import sys
from lexer import TokenType, Token, Lexer
from parse import Parser

if len(sys.argv) < 2:
    print('[ERROR]: No argument supplied!')
    print('[ARGUMENT]: <file_path>')
    sys.exit()

file_path = sys.argv[1]
source = None

with open(file_path) as file:
    source = file.read()

lexer = Lexer(source, file_path)
parser = Parser(lexer)

parser.program()
