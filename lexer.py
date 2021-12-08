import sys
from enum import Enum

class TokenType(Enum):
    EOF = 0
    CHAR_NEWLINE = 1
    BINOP_PLUS = 2
    BINOP_MINUS = 3
    BINOP_MUL = 4
    BINOP_DIV = 5
    LITERAL_NUMBER = 6
    LITERAL_STRING = 7
    KEYWORD_DEFINE = 8
    EQUAL = 9
    COMP_EQEQ = 10
    COMP_NTEQ = 11
    COMP_LT = 11
    COMP_GT = 12
    COMP_LTEQ = 13
    COMP_GTEQ = 14
    STATEMENT_PRINT = 15
    IDENTIFIER = 16

class Token:
    def __init__(self, tk, rep):
        self.type = tk
        self.repr = rep

class Lexer:
    def __init__(self, source, file_name):
        self.source = source.strip()
        self.file_name = file_name
        self.current_index = 0
        self.current_line = 1
        self.current_char = self.source[self.current_index]

    def error_and_die(self, message):
        print(f"File: \"<{self.file_name}>\"")
        print(f"[ERROR]: {message}, at Line: {self.current_line}")
        sys.exit(1)

    def advance(self):
        self.current_index += 1

        if self.current_index >= len(self.source):
            self.current_char = '\0'
        elif self.current_char == '\n':
            self.current_line += 1
            self.current_char = self.source[self.current_index]
        else:
            self.current_char = self.source[self.current_index]

    def skip_whitespaces(self):
        while self.current_char == ' ' or self.current_char == '\t' or self.current_char == '\r':
            self.advance()

    def skip_comments(self):
        if self.current_char == '#':
            while self.current_char != '\n' and self.current_char != '\0':
                self.advance()

    def peek_character(self):
        if self.current_index >= len(self.source):
            return '\0'
        else:
            return self.source[self.current_index + 1]

    def get_token(self):
        self.skip_whitespaces()
        self.skip_comments()

        token = None

        if self.current_char == '\0':
            token = Token(TokenType.EOF, None)

        elif self.current_char == '\n':
            token = Token(TokenType.CHAR_NEWLINE, None)

        elif self.current_char == '+':
            token = Token(TokenType.BINOP_PLUS, self.current_char)

        elif self.current_char == '-':
            token = Token(TokenType.BINOP_MINUS, self.current_char)

        elif self.current_char == '*':
            token = Token(TokenType.BINOP_MUL, self.current_char)

        elif self.current_char == '/':
            token = Token(TokenType.BINOP_DIV, self.current_char)

        elif self.current_char == '=':
            if self.peek_character() != '\0' and self.peek_character() == '=':
                self.advance()
                token = Token(TokenType.COMP_EQEQ, '==')
            else:
                token = Token(TokenType.EQUAL, self.current_char)

        elif self.current_char == '!':
            if self.peek_character() != '\0' and self.peek_character() == '=':
                self.advance()
                token = Token(TokenType.COMP_NTEQ, '!=')
            else:
                self.error_and_die(f"expected != but got \"{self.current_char}\"")

        elif self.current_char == '<':
            if self.peek_character() != '\0' and self.peek_character() == '=':
                self.advance()
                token = Token(TokenType.COMP_LTEQ, '<=')
            else:
                token = Token(TokenType.LT, self.current_char)

        elif self.current_char == '>':
            if self.peek_character() != '\0' and self.peek_character() == '=':
                self.advance()
                token = Token(TokenType.COMP_GTEQ, '>=')
            else:
                token = Token(TokenType.GT, self.current_char)

        # Search for string
        elif self.current_char == '"':
            start_pos = self.current_index
            string = ''
            self.advance()

            while self.current_char != '"' and self.current_char != '\0' and self.current_char != '\n':
                string += self.current_char
                self.advance()

            end_pos = self.current_index

            if self.current_char == '\0' or self.current_char == '\n':
                self.error_and_die(f"( {self.source[start_pos:end_pos:]} ) \nmissing double quotes after opening quotes")

            token = Token(TokenType.LITERAL_STRING, string)

        # Search for number
        elif self.current_char >= '0' and self.current_char <= '9':
            decimal_count = 0
            num_str = ''
            num_str += self.current_char
            self.advance()

            # Keep appending if current character is number
            while (self.current_char >= '0' and self.current_char <= '9') or self.current_char == '.':
                if self.current_char == '.':
                    decimal_count += 1
                    if decimal_count >= 2:
                        self.error_and_die(f"unexpected token \"{self.current_char}\" before {num_str}")

                num_str += self.current_char
                self.advance()

            if num_str.endswith('.'):
                num_str += '0'

            token = Token(TokenType.LITERAL_NUMBER, num_str)

        # Search for identifier or keyword
        elif (self.current_char >= 'a' and self.current_char <= 'z') or self.current_char >= 'A' and self.current_char <= 'Z':
            identifier_str = ''
            identifier_str += self.current_char
            self.advance()

            while (self.current_char >= 'a' and self.current_char <= 'z') or self.current_char >= 'A' and self.current_char <= 'Z':
                identifier_str += self.current_char
                self.advance()

            if identifier_str == 'define':
                token = Token(TokenType.KEYWORD_DEFINE, identifier_str)
            elif identifier_str == 'print':
                token = Token(TokenType.STATEMENT_PRINT, identifier_str)
            else:
                token = Token(TokenType.IDENTIFIER, identifier_str)
        else:
            self.error_and_die(f"unexpected token \"{self.current_char}\"")

        self.advance()

        return token
