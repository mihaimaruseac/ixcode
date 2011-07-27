# IxCode - app for code spelunking :: block diagram
# Transform functions to the corresponding block diagram

def build_dot_string(frepr):
    """
    Constructs the input for DOT given a function representation.

        frepr - representation of function
        --
        returns: function representation
    """
    s = 'digraph{\n\tnode [shape=box];\n'
    import pdb
    pdb.set_trace()
    return s + '}\n'

def dot(fcts):
    """
    Transform each function to the graphical representation.

        fcts - list of functions to transform
        --
        returns: None
    """
    for fname, frepr in fcts:
        print fname, frepr
        print build_dot_string(frepr)

