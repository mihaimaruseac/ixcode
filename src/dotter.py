# IxCode - app for code spelunking :: block diagram
# Transform functions to the corresponding block diagram

class BB:
    """
    A basic block. To be displayed by itself in the diagram.
    """
    def __init__(self, leader, instrs):
        """
        leader  -   leader of block
        instrs  -   instructions from the block
        """
        self._id = id(leader)
        self._leader = leader
        self._instrs = instrs

    def __str__(self):
        return '(%d)%s->%d' % (self._id, self._leader, len(self._instrs))

    def __repr__(self):
        return '>%s<' % self.__str__()

def get_leaders(block, leaders):
    instrs = block.instrs()

    next_leader = False
    for i in instrs:
        if next_leader:
            next_leader = False
            i.set_leader()
        if i.is_leader():
            leaders[id(i)] = i
        if i.is_block():
            get_leaders(i.block(), leaders)
        if i.is_jump():
            next_leader = True

def build_dot_string(frepr):
    """
    Constructs the input for DOT given a function representation.

        frepr - representation of function
        --
        returns: function representation
    """
    block = frepr.block()

    # get leaders
    leaders = {}
    get_leaders(block, leaders)
    print leaders

#    block_dict = {} # block dictionary
#    dot_block(block, block_dict)
#    print block_dict

    s = 'digraph{\n\tnode [shape=box];\n'
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

