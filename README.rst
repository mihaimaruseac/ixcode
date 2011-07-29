Ixcode
======

A. About
........

This utility parses source files and constructs diagrams for each interesting
function found. This diagram shows the basic blocks of that function making it
easier to understand what the code is doing. Also, this can help in
refactoring.

It is written in Python and requires PLY to be installed. On Ubuntu, the
``python-ply`` package is enough. the diagrams are created using DOT, thus
``graphviz`` has to be installed too.

B. Usage
........

Running ``ixcode`` without arguments a short usage will be given. Full usage is
given by passing ``-h``.

A run needs at least the name of the file to be parsed. The user can supply a
list of interesting functions, only them would be graphed later.

C. Bugs
.......

1. Some diagrams are hard to understand without using colors. It is a DOT
   limitation though.

1. This tool assumes that the code compiles successfully. It uses a more
   permissive grammar than C's and may give wrong results if the code is not
   legal.

D. TODO
.......

1. Parse enums, structs and unions

1. Parse and graph ``switch``, ``case``, ``continue`` and ``break``.

1. Add a config file for colors

1. Add support for Python too.

