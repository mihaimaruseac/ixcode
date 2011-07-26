# IxCode - app for code spelunking :: block diagram
# Data for lexing C code.

from ply.lex import TOKEN

# Define keywords here
keywords = [
        'AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST', 'CONTINUE', 'DEFAULT','DO',
        'DOUBLE', 'ELSE', 'ENUM', 'EXTERN', 'FLOAT', 'FOR', 'GOTO', 'IF',
        'INLINE', 'INT', 'LONG', 'REGISTER', 'RESTRICT', 'RETURN', 'SHORT',
        'SIGNED', 'SIZEOF', 'STATIC', 'STRUCT', 'SWITCH', 'TYPEDEF', 'UNION',
        'UNSIGNED', 'VOID', 'VOLATILE', 'WHILE'
        ]

keyword_map = {}
for r in keywords:
    keyword_map[r.lower()] = r

# Define token names here
tokens = keywords + [
        'ID', # identifier, reserved keyword or name
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
        'OR', 'AND', 'NOT', 'XOR',
        'LSHIFT', 'RSHIFT', 'LOR', 'LAND', 'LNOT',
        'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
        'EQUALS', 'PLUSEQUAL', 'MINUSEQUAL',
        'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL',
        'LSHIFTEQUAL', 'RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL', 'OREQUAL',
        'PLUSPLUS', 'MINUSMINUS',
        'ARROW', 'CONDOP',
        'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE',
        'COMMA', 'PERIOD', 'SEMI', 'COLON', 'ELLIPSIS', 'LINECONT', 'PPHASH',
        'INT_CONST_DEC', 'INT_CONST_OCT', 'INT_CONST_HEX',
        'FLOAT_CONST', 'CHAR_CONST', 'STRING_LITERAL'
        ]

# Construct lang_lex_dict dictionary
lang_lex_dict = {}
lang_lex_dict['tokens'] = tokens

states = lang_lex_dict['states'] = (
        ('ppline', 'exclusive'),
        )

def t_ppline_LINE(self, t):
    r'[^\\\n]+'
    return None

def t_ppline_EXTEND(self, t):
    r'\\\n'
    return None

def t_ppline_NEWLINE(self, t):
    r'\n'
    t.lexer.begin('INITIAL')

def t_ppline_error(self, t):
    self.t_error(t)

def t_COMMENT(self, t):
    r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
    """
    Return None to skip
    """
    return None

def t_NEWLINE(self, t):
    r'\n+'
    """
    Increment line count.
    """
    t.lexer.lineno += t.value.count('\n')

def t_LINECONT(self, t):
    r'\\'
    """
    Increment line count.
    """
    t.lexer.lineno += 1

def t_PPHASH(self, t):
    r'\#'
    """
    Strip these lines
    """
    t.lexer.begin('ppline')

def t_ID(self, t):
    r'[a-zA-Z_][0-9a-zA-Z_]*'
    """
    Changes token's type if token is keyword, otherwise leaves it as ID.
    """
    t.type = keyword_map.get(t.value, 'ID')
    return t

int_suffix = r'(u?ll|U?LL|([uU][lL])|([lL][uU])|[uU]|[lL])?'
dec_ct = '(0' + int_suffix + ')|([1-9][0-9]*' + int_suffix + ')'
oct_ct = '0[0-7]*' + int_suffix
hex_ct = '0[xX][0-9a-fA-F]+' + int_suffix
bad_oct = '0[0-7]*[89]'

simple_escape = r"""([a-zA-Z\\?'"])"""
octal_escape = r"""([0-7]{1,3})"""
hex_escape = r"""(x[0-9a-fA-F]+)"""
bad_escape = r"""([\\][^a-zA-Z\\?'"x0-7])"""
escape = r"""(\\(""" + simple_escape + '|' + octal_escape + '|'\
        + hex_escape + '))'

cconst_char = r"""([^'\\\n]|""" + escape + ')'
char_const = "'" + cconst_char + "'"
unmatched_quote = "('" + cconst_char + "*\\n)|('" + cconst_char + "*$)"
bad_char_const = r"""('""" + cconst_char + """[^'\n]+')|('')|('"""\
        + bad_escape + r"""[^'\n]*')"""

cstring = r"""([^"\\\n]|""" + escape + ')'
string = '"' + cstring + '*"'
bad_string = '"' + cstring + '*' + bad_escape + cstring + '*"'

exponent = r"""([eE][-+]?[0-9]+)"""
fract = r"""([0-9]*\.[0-9]+)|([0-9]+\.)"""
flt = '((((' + fract + ')' + exponent + '?)|([0-9]+' + exponent + '))[FfLl]?)'

@TOKEN(flt)
def t_FLOAT_CONST(self, t):
    return t

@TOKEN(hex_ct)
def t_INT_CONST_HEX(self, t):
    return t

@TOKEN(bad_oct)
def t_BAD_CONST_OCT(self, t):
   msg = 'Invalid octal constant '
   self.error(msg, t)

@TOKEN(oct_ct)
def t_INT_CONST_OCT(self, t):
    return t

@TOKEN(dec_ct)
def t_INT_CONST_DEC(self, t):
    return t

@TOKEN(char_const)
def t_CHAR_CONST(self, t):
    return t

@TOKEN(unmatched_quote)
def t_UNMATCHED_QUOTE(self, t):
    msg = "Unmatched '"
    self.error(msg, t)

@TOKEN(bad_string)
def t_BAD_STRING_LITERAL(self, t):
    msg = "Invalid escape code in string"
    self.error(msg, t)

@TOKEN(string)
def t_STRING_LITERAL(self, t):
    return t

t_ignore = t_ppline_ignore = ' \t'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_OR = r'\|'
t_AND = r'&'
t_NOT = r'~'
t_XOR = r'\^'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_LOR = r'\|\|'
t_LAND = r'&&'
t_LNOT = r'!'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_EQUALS = r'='
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'-='
t_TIMESEQUAL = r'\*='
t_DIVEQUAL = r'/='
t_MODEQUAL = r'%='
t_LSHIFTEQUAL = r'<<='
t_RSHIFTEQUAL = r'>>='
t_ANDEQUAL = r'&='
t_OREQUAL = r'\|='
t_XOREQUAL = r'\^='
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'
t_ARROW = r'->'
t_CONDOP = r'\?'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = ','
t_PERIOD = r'\.'
t_SEMI = r';'
t_COLON = r':'
t_ELLIPSIS = r'\.\.\.'

