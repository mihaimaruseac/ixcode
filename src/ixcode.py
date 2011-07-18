# IxCode - app for code spelunking :: block diagram
# Overmind

import c.ixcode as c
import python.ixcode as python

def main(filename, functions, opts, err):
    if opts.type == 'C':
        c.main(filename, functions, opts, err)
    elif opts.type == 'Python':
        python.main(filename, functions, opts, err)

