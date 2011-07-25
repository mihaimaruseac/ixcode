# IxCode - app for code spelunking :: block diagram
# C specific code version of the tool

import sys

from lexer_data import lang_lex_dict
import parser_data

_d = sys.modules['src.c.parser_data'].__dict__
lang_parse_dict = {}
for k in _d:
    if k[:2] == 'p_':
        lang_parse_dict[k] = _d[k]

# Change here if not starting from `file'
lang_parse_dict['start'] = 'file'

