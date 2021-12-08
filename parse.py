from lexer import TokenType, Token, Lexer

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.current_token = None
        self.peek_token = None

        self.next_token()
        self.next_token()

    def check_token(self, kind):
        return kind == self.current_token.type

    def check_peek(self, kind):
        return kind == self.peek_token.type

    def match(self, kind):
        if not self.check_token(kind):
            self.error_and_die(f"expected {kind}, got {self.current_token.type}")
        self.next_token()

    def next_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def program(self):
        while self.check_token(TokenType.CHAR_NEWLINE):
            self.next_token()

        while not self.check_token(TokenType.EOF):
            self.statement()

    def statement(self):
        if self.check_token(TokenType.CHAR_NEWLINE):
            self.next_token()

        elif self.check_token(TokenType.KEYWORD_PRINT):
            print("STATEMENT_PRINT")
            self.next_token()

            if self.check_token(TokenType.LITERAL_STRING):
                self.next_token()
            else:
                self.expression()

        # Assigning variable
        elif self.check_token(TokenType.KEYWORD_DEFINE):
            print("STATEMENT_DEFINE")
            self.next_token()
            self.match(TokenType.IDENTIFIER)
            self.match(TokenType.EQUAL)
            self.expression()

        # Support reassign variable
        elif self.check_token(TokenType.IDENTIFIER):
            self.next_token()
            self.match(TokenType.EQUAL)
            self.expression()

        elif self.check_token(TokenType.KEYWORD_IF):
            print("STATEMENT_IF")
            self.next_token()
            self.comparison()
            self.match(TokenType.KEYWORD_THEN)

            while not self.check_token(TokenType.KEYWORD_ENDIF) or self.check_token(TokenType.EOF):
                self.statement()

            self.match(TokenType.KEYWORD_ENDIF)

        else:
            self.error_and_die(f"invalid statement at {self.current_token.repr} ({self.current_token.type})")

    def expression(self):
        print("EXPRESSION")

        self.term()

        while self.check_token(TokenType.BINOP_PLUS) or self.check_token(TokenType.BINOP_MINUS):
            self.next_token()
            self.term()

    def term(self):
        print("TERM")

        self.unary()

        while self.check_token(TokenType.BINOP_MUL) or self.check_token(TokenType.BINOP_DIV):
            self.next_token()
            self.unary()

    def unary(self):
        print(f"UNARY ({self.current_token.repr})")

        if self.check_token(TokenType.BINOP_PLUS) or self.check_token(TokenType.BINOP_MINUS):
            self.next_token()
        self.primary()

    def primary(self):
        print(f"PRIMARY ({self.current_token.repr})")

        if self.check_token(TokenType.LITERAL_NUMBER):
            self.next_token()
        elif self.check_token(TokenType.LITERAL_STRING):
            self.next_token()
        elif self.check_token(TokenType.IDENTIFIER):
            self.next_token()
        else:
            self.error_and_die(f"unexpected token at {self.current_token.repr}")

    def newline(self):
        self.match(TokenType.CHAR_NEWLINE)
        while self.check_token(TokenType.CHAR_NEWLINE):
            self.next_token()

    def comparison(self):
        print("COMPARISON")

        self.expression()

        if self.is_comparison_operator():
            self.next_token()
            self.expression()
        else:
            self.error_and_die(f"expected comparison operator after: {self.current_token.repr}")

        while self.is_comparison_operator():
            self.next_token()
            self.expression()

    def is_comparison_operator(self):
        return self.check_token(TokenType.COMP_EQEQ) or self.check_token(TokenType.COMP_NTEQ) or self.check_token(TokenType.COMP_LT) or self.check_token(TokenType.COMP_GT) or self.check_token(TokenType.COMP_LTEQ) or self.check_token(TokenType.COMP_GTEQ)

    def error_and_die(self, message):
        self.lexer.error_and_die(message);

