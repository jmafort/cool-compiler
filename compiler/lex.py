from ply import lex
from ply.lex import LexToken


class LexicalAnalyzer:
     
    tokens = [ 
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'EQUALS',
        'LESSTHAN',
        'LESSOREQUAL',
        'ASSIGNMENT',
        'ARROW',
        'STRING',
        'INTEGER',
        'TRUE',
        'FALSE',
        'COLON',
        'DOT',
        'COMMA',
        'SEMICOLON',
        'AT',
        'TILDE',
        'LBRACKET',
        'RBRACKET',
        'LPAREN',
        'RPAREN',
        'ID',
        'TYPE',
        'SELF',
        'WHITE_SPACE'
    ]

    reserved_words = {
        "class": "CLASS",
        "else": "ELSE",
        "fi": "FI",
        "if": "IF",
        "in": "IN",
        "inherits": "INHERITS",
        "isvoid": "ISVOID",
        "let": "LET",
        "loop": "LOOP",
        "pool": "POOL",
        "then": "THEN",
        "while": "WHILE",
        "case": "CASE",
        "esac": "ESAC",
        "new": "NEW",
        "of": "OF",
        "not": "NOT"
    }

    tokens += reserved_words.values()

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_EQUALS  = r'='
    t_LESSTHAN = r'<'
    t_LESSOREQUAL = r'<='
    t_ASSIGNMENT = r'<-'
    t_ARROW = r'=>'
    t_COLON = r':'
    t_DOT = r'\.' 
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_AT = r'@'
    t_TILDE = r'~'
    t_LBRACKET = r'\{'
    t_RBRACKET = r'\}'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_FALSE = r'f(a|A)(l|L)(s|S)(e|E)'
    t_TRUE = r't(r|R)(u|U)(e|E)'

    def __init__(self):
        """
        Building a stat tracker.
        """

        self.integers: int = 0
        self.strings: int = 0
        self.comments: int = 0
        self.types: int = 0
        self.unique_types: list = []

    def t_COMMENT(self, token) -> None:
        r"""
        \(\*(.|\n)*\*\)
        """

        self.comments += 1
        return None

    def t_COMMENT_INLINE(self, token) -> None:
        r"""
        --.*\n?
        """
        
        self.comments += 1
        return None
    
    @staticmethod
    def t_WHITE_SPACE(token) -> None:
        r"""
        \ |\f|\r|\t|\v
        """
        
        return None

    @staticmethod
    def t_NEWLINE(token) -> None:
        r"""
        \n+
        """
        
        token.lexer.lineno += len(token.value)
        return None

    def t_STRING(self, token) -> LexToken:
        r"""
        "[^"\0\n]*((\\\n)|[^"\0\n])*"
        """

        self.strings += 1
        return token

    def t_INTEGER(self, token) -> LexToken:
        r"""
        \d+
        """

        token.value = int(token.value)
        self.integers += 1
        return token

    def t_ID(self, token):
        r"""
        [a-zA-Z][a-zA-Z_0-9]*
        """

        if token.value[0].isupper():
            token.type = 'TYPE'
            self.types += 1
            self.unique_types += [token.value]
        if token.value == 'SELF_TYPE':
            token.type = 'TYPE'
        elif token.value == 'self':
            token.type = 'SELF'
        elif token.value.lower() in self.reserved_words.keys():
            token.type = self.reserved_words[token.value.lower()]

        return token

    @staticmethod
    def t_error(token) -> None:
        print(f'Illegal character: [{token.value[0]}]')
        token.lexer.skip(1)

    def build(self, **kwargs) -> None:
        self.lexer = lex.lex(module=self, **kwargs)
    
    def parse(self, data) -> None:
        self.lexer.input(data)
        
        while True:
            token = self.lexer.token()
            if not token: 
                break
            
            print(token)

        print(
            '\n'
            f'INTERGERS found: {self.integers}\n'
            f'STRINGS found: {self.strings}\n'
            f'COMMENTS found: {self.comments}\n'
            f'TYPES found: {self.types}\n'
            f'Unique TYPES found: {list(dict.fromkeys(self.unique_types))}'
            '\n'
        )