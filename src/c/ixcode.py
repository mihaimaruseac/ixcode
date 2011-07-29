# IxCode - app for code spelunking :: block diagram
# C specific code version of the tool

import sys

import lexer_data
import parser_data

_d = sys.modules['src.c.lexer_data'].__dict__
lang_lex_dict = {}
for k in _d:
    if k[:2] == 't_':
        lang_lex_dict[k] = _d[k]

lang_lex_dict['tokens'] = _d['tokens']
lang_lex_dict['states'] = _d['states']
lang_lex_dict['language'] = 'C'

_d = sys.modules['src.c.parser_data'].__dict__
lang_parse_dict = {}
for k in _d:
    if k[:2] == 'p_':
        lang_parse_dict[k] = _d[k]

lang_parse_dict['start'] = _d['start']
lang_parse_dict['precedence'] = _d['precedence']
lang_parse_dict['language'] = 'C'

