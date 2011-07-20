# IxCode - app for code spelunking :: block diagram
# AST from C code.

# Do this unsafe import to inject this code
from src.ast import *

class Include(Node):
    """
    An include declaration, holds the included filename (assumed to be
    correct).
    """
    def __init__(self, fname):
        self._fname = fname

    def __str__(self):
        return '#include <%s>' % self._fname

