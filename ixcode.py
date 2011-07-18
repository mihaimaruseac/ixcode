#!/usr/bin/env python
#
# Entry point for IxCode - app for code spelunking

# TODO: optparse is deprecated from 2.7, if we ever switch to 3.0+ change to
# argparse (code doesn't need to change that much)
import optparse

__PROG__ = 'IxCode'
__VERSION__ = '0.0'
__FILETYPES__ = ['C', 'Python', 'c', 'cpp', 'py']

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
    print opts
    fileName, functions = extra[0], extra[1:]
    print fileName, functions

if __name__ == '__main__':
    main()

