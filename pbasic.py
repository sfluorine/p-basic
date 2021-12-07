#!/usr/bin/env pypy3

import sys
from lexer import Lexer, TokenType

if len(sys.argv) < 2:
    print('[ERROR]: No argument supplied!')
    print('[ARGUMENT]: <file_path>')
    sys.exit()

file_path = sys.argv[1]
source = None

with open(file_path) as file:
    source = file.read()

lexer = Lexer(source, file_path)
token = lexer.get_token()

while token.type != TokenType.EOF:
    if token.type != TokenType.CHAR_NEWLINE:
        print(f"{token.type}: {token.repr}")
    token = lexer.get_token()
