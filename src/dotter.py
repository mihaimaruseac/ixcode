# IxCode - app for code spelunking :: block diagram
# Transform functions to the corresponding block diagram

import os

START = -1
END = -42

class BB:
    """
    A basic block. To be displayed by itself in the diagram.
    """
    def __init__(self, bid, leader=None, instrs=None):
        """
        leader  -   leader of block
        instrs  -   instructions from the block
        """
        self.bid = bid
        self._leader = leader
        self._instrs = instrs

    def description(self):
        s = ''
        if not self._instrs:
            if self.bid == START:
                return '<<start>>'
            elif self.bid == END:
                return '<<end>>'
            else:
                return s
        for i in self._instrs:
            tmp = '%s' % i
            tmp = tmp.replace('\\', '\\\\')
            tmp = tmp.replace('"', '\\"')
            s += '%s\\n' % tmp
        return s

    def __str__(self):
        return '(%d)%s: [%s]' % (self.bid, self._leader, self._instrs)

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

def get_blocks(block, leaders, blocks):
    instrs = block.instrs()

    last_leader = None
    bbi = []
    for i in instrs:
        if id(i) in leaders:
            if last_leader:
                blocks.append(BB(id(last_leader), last_leader, bbi))
                bbi = []
            last_leader = i
        if i.is_block():
            get_blocks(i.block(), leaders, blocks)
        if not (i.is_block() or i.is_jump()):
            bbi.append(i)
    if last_leader:
        blocks.append(BB(id(last_leader), last_leader, bbi))

def get_links(block, leaders, blocks, links):
    instrs = block.instrs()

    instructions = []
    prev = None
    for i in instrs:
        if id(i) in leaders:
            prev = i
        for b in blocks:
            if not b._instrs:
                continue
            if i in b._instrs:
                break
        else:
            instructions.append((i, prev))
    print instructions
    print blocks

    for i, p in instructions:
        jumps = i.insides(links)
        if p:
            for j in jumps:
                links[(id(p), j[0])] = j[1]
        else:
            for j in jumps:
                links[(START, j[0])] = j[1]

#    for i, p in instructions:
#        jumps = i.jumps()
#        if p:
#            links[(id(p), i.block().get_bb_id())] = ''
#        else:
#            links[(START, i.block().get_bb_id())] = ''

#    for i in instrs:
#        if id(i) in leaders:
#            id_bb = id(i)
##            for (l, d) in to_link:
##                links[(l, id_bb)] = d
##            to_link = []
##        bb_links = i.get_links()
##        for dest, desc in bb_links:
##            if dest:
##                links[(id_bb, dest)] = desc
##            else:
##                to_link = [(id_bb, ''), (i.block().get_bb_id(), desc)]
#        if i.is_block():
#           get_links(i.block(), leaders, blocks, links, False)

def build_dot_string(blocks, links):
    """
    Constructs the input for DOT given a function representation.

        frepr - representation of function
        --
        returns: function representation
    """
    s = 'digraph{\n\tnode [shape=box];\n'
    for b in blocks:
        s += '\t%d [label="%s"];\n' % (b.bid, b.description())

    if 0 in map(lambda p:p[1], links):
        s += '\t0 [label="", shape="point"];\n'

    for l in links:
        d = links[l]
        s += '\t%d -> %d' % l
        if d:
            s += ' [label="%s"]' % d
        s += ';\n'

    return s + '}\n'

def dot(fcts):
    """
    Transform each function to the graphical representation.

        fcts - list of functions to transform
        --
        returns: None
    """
    for fname, frepr in fcts:
        block = frepr.block()

        # get leaders
        leaders = {}
        get_leaders(block, leaders)

        # get BBs
        blocks = []
        get_blocks(block, leaders, blocks)
        blocks.append(BB(START))
        blocks.append(BB(END))

        # obtain links
        links = {}
        get_links(block, leaders, blocks, links)

        s = build_dot_string(blocks, links)

        filename = '%s.dot' % fname
        with open(filename, 'w') as f:
            f.write(s)
        os.system('dot -Tpng %s > %s.png' % (filename, fname))

