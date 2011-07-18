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

def check_type(filename, filetype, parser):
    if not filetype:
        import mimetypes
        filetype = mimetypes.guess_type(filename)
        if filetype[0] == 'text/x-csrc':
            return 'C'
        elif filetype[0] == 'text/x-python':
            return 'Python'
        else:
            parser.error('Unable to guess filetype, please use -t / --type')
    elif filetype in ['C', 'c', 'cpp']:
        return 'C'
    elif filetype in ['Python', 'py']:
        return 'Python'
    else:
        parser.error('Unable to guess filetype, please use -t / --type')

def build_parser():
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

    return parser

def main():
    parser = build_parser()
    (opts, extra) = parser.parse_args()

    if not extra:
        parser.error('Missing filename')
    filename, functions = extra[0], extra[1:]
    if not os.path.isfile(filename):
        parser.error('%s - No such file' % filename)
    opts.type = check_type(filename, opts.type, parser)
    print filename, functions
    ixcode.test()

if __name__ == '__main__':
    main()

