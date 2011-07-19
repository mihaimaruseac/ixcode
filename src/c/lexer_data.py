# IxCode - app for code spelunking :: block diagram
# Data for lexing C code.

lang_lex_dict = {}
lang_lex_dict['t_HASH'] = r'\#'
lang_lex_dict['keywords'] = [
        'INCLUDE'
        ]
lang_lex_dict['tokens'] = lang_lex_dict['keywords'] + [
        'HASH' # #
        ]

