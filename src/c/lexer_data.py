# IxCode - app for code spelunking :: block diagram
# Data for lexing C code.

from ply.lex import TOKEN

# Define keywords here
keywords = [
        'AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST', 'CONTINUE', 'DEFAULT','DO',
        'DOUBLE', 'ELSE', 'ENUM', 'EXTERN', 'FLOAT', 'FOR', 'GOTO', 'IF',
        'INLINE', 'INT', 'LONG', 'REGISTER', 'RESTRICT', 'RETURN', 'SHORT',
        'SIGNED', 'SIZEOF', 'STATIC', 'STRUCT', 'SWITCH', 'TYPEDEF', 'UNION',
        'UNSIGNED', 'VOID', 'VOLATILE', 'WHILE',
        'DEFINE', 'IFDEF', 'IFNDEF', 'ENDIF', 'INCLUDE'
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

# Add each t_TOKEN to lang_lex_dict dictionary
lang_lex_dict['t_ignore'] = ' \t'
lang_lex_dict['t_COMMENT'] = t_COMMENT
lang_lex_dict['t_NEWLINE'] = t_NEWLINE
lang_lex_dict['t_ID'] = t_ID
lang_lex_dict['t_PLUS'] = r'\+'
lang_lex_dict['t_MINUS'] = r'-'
lang_lex_dict['t_TIMES'] = r'\*'
lang_lex_dict['t_DIVIDE'] = r'/'
lang_lex_dict['t_MOD'] = r'%'
lang_lex_dict['t_OR'] = r'\|'
lang_lex_dict['t_AND'] = r'&'
lang_lex_dict['t_NOT'] = r'~'
lang_lex_dict['t_XOR'] = r'\^'
lang_lex_dict['t_LSHIFT'] = r'<<'
lang_lex_dict['t_RSHIFT'] = r'>>'
lang_lex_dict['t_LOR'] = r'\|\|'
lang_lex_dict['t_LAND'] = r'&&'
lang_lex_dict['t_LNOT'] = r'!'
lang_lex_dict['t_LT'] = r'<'
lang_lex_dict['t_LE'] = r'<='
lang_lex_dict['t_GT'] = r'>'
lang_lex_dict['t_GE'] = r'>='
lang_lex_dict['t_EQ'] = r'=='
lang_lex_dict['t_NE'] = r'!='
lang_lex_dict['t_EQUALS'] = r'='
lang_lex_dict['t_PLUSEQUAL'] = r'\+='
lang_lex_dict['t_MINUSEQUAL'] = r'-='
lang_lex_dict['t_TIMESEQUAL'] = r'\*='
lang_lex_dict['t_DIVEQUAL'] = r'/='
lang_lex_dict['t_MODEQUAL'] = r'%='
lang_lex_dict['t_LSHIFTEQUAL'] = r'<<='
lang_lex_dict['t_RSHIFTEQUAL'] = r'>>='
lang_lex_dict['t_ANDEQUAL'] = r'&='
lang_lex_dict['t_OREQUAL'] = r'\|='
lang_lex_dict['t_XOREQUAL'] = r'\^='
lang_lex_dict['t_PLUSPLUS'] = r'\+\+'
lang_lex_dict['t_MINUSMINUS'] = r'--'
lang_lex_dict['t_ARROW'] = r'->'
lang_lex_dict['t_CONDOP'] = r'\?'
lang_lex_dict['t_LPAREN'] = r'\('
lang_lex_dict['t_RPAREN'] = r'\)'
lang_lex_dict['t_LBRACKET'] = r'\['
lang_lex_dict['t_RBRACKET'] = r'\]'
lang_lex_dict['t_LBRACE'] = r'\{'
lang_lex_dict['t_RBRACE'] = r'\}'
lang_lex_dict['t_COMMA'] = r','
lang_lex_dict['t_PERIOD'] = r'\.'
lang_lex_dict['t_SEMI'] = r';'
lang_lex_dict['t_COLON'] = r':'
lang_lex_dict['t_ELLIPSIS'] = r'\.\.\.'
lang_lex_dict['t_LINECONT'] = t_LINECONT
lang_lex_dict['t_PPHASH'] = r'\#'
lang_lex_dict['t_FLOAT_CONST'] = t_FLOAT_CONST
lang_lex_dict['t_INT_CONST_HEX'] = t_INT_CONST_HEX
lang_lex_dict['t_BAD_CONST_OCT'] = t_BAD_CONST_OCT
lang_lex_dict['t_INT_CONST_OCT'] = t_INT_CONST_OCT
lang_lex_dict['t_INT_CONST_DEC'] = t_INT_CONST_DEC
lang_lex_dict['t_CHAR_CONST'] = t_CHAR_CONST
lang_lex_dict['t_UNMATCHED_QUOTE'] = t_UNMATCHED_QUOTE
lang_lex_dict['t_BAD_STRING_LITERAL'] = t_BAD_STRING_LITERAL
lang_lex_dict['t_STRING_LITERAL'] = t_STRING_LITERAL

