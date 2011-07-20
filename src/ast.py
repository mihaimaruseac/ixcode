# IxCode - app for code spelunking :: block diagram
# Generic AST.

class Node:
    """
    Base class for all nodes in AST. All methods raise exceptions to ensure
    proper derivation.
    """
    def __str__(self):
        raise NotImplementedError()


