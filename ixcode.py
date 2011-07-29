#!/usr/bin/env python
#
# IxCode - app for code spelunking :: block diagram
# Entry point

# TODO: optparse is deprecated from 2.7, if we ever switch to 3.0+ change to
# argparse (code doesn't need to change that much)

import optparse
import os
import src.ixcode as ixcode

__PROG__ = 'IxCode'
__VERSION__ = '0.0'
__FILETYPES__ = ['C', 'Python', 'c', 'cpp', 'py']

def check_type(filename, filetype, arg_err):
    """
    Checks type of filename. If it was given in the command line uses this,
    otherwise guesses bassed on MIME.

    Returns a standardized view of the language used. For now, returns the
    name of the language (C++ and C must be C for now).

        filename - filename to detect
        filetype - assumed filetype
        arg_err - callback for errors caused by a command line argument
        --
        returns: type of filename as a string representing the language used.
    """
    if not filetype:
        import mimetypes
        filetype = mimetypes.guess_type(filename)
        if filetype[0] == 'text/x-csrc':
            return 'C'
        elif filetype[0] == 'text/x-python':
            return 'Python'
        else:
            arg_err('Unable to guess filetype, please use -t / --type')
    elif filetype in ['C', 'c', 'cpp']:
        return 'C'
    elif filetype in ['Python', 'py']:
        return 'Python'
    else:
        arg_err('Unable to guess filetype, please use -t / --type')

def build_parser():
    """
    Builds the option parses for command line arguments. Change here if you
    want to add more options.

        --
        returns: parser
    """
    description = '%prog - utility for code spelunking: transform function' +\
            ' to basic block jump tree using PLY and dot.'
    prog = __PROG__
    epilog = 'Report bugs to mmaruseac@ixiacom.com / mihai@rosedu.org'
    version = '%prog ' + __VERSION__
    usage = 'usage: %prog FILE [options] FUNCTIONS'

    parser = optparse.OptionParser(
            description=description,
            prog=prog,
            usage=usage,
            version=version,
            epilog=epilog)

    parser.add_option('-t', '--type',
            help='type of filename',
            dest='type',
            choices=__FILETYPES__)

    parser.add_option('-d', '--debug',
            help='debug grammar',
            dest='debug',
            action='store_true')

    parser.add_option('-o', '--outdir',
            help='output directory',
            default='.',
            dest='outdir')

    return parser

def remove(basename):
    """
    Removes Python files starting with basename adding py and pyc extensions.
    """
    fs = ['%s.py' % basename, '%s.pyc' % basename]
    for f in fs:
        if os.path.exists(f):
            os.remove(f)

def cleanup_old_grammars(lang):
    """
    Removes old grammar files since we are debugging a new grammar, probably a
    new entered grammar.
    """
    lextab = '%slextab' % lang
    parsetab = '%sparsetab' % lang
    remove(lextab)
    remove(parsetab)

def main():
    """
    Main entry point.
    """
    parser = build_parser()
    (opts, extra) = parser.parse_args()
    error = lambda x: parser.error(x)

    if not extra:
        error('Missing filename')
    filename, functions = extra[0], extra[1:]
    if not os.path.isfile(filename):
        error('%s - No such file' % filename)
    opts.type = check_type(filename, opts.type, error)
    debug = opts.debug
    del opts.debug
    if debug:
        cleanup_old_grammars(opts.type)
    ixcode.main(filename, functions, opts, error, debug)

if __name__ == '__main__':
    main()

