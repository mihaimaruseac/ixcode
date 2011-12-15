# IxCode - app for code spelunking :: block diagram
# Transform functions to the corresponding block diagram

import os

import ast

START = -1
END = -2

def fix(string):
    """
    Escapes several entities form the passed in string to ensure proper DOT
    output.
    """
    string = string.replace('\\', '\\\\')
    string = string.replace('"', '\\"')
    return string

def get_leaders(block, leaders):
    instrs = block.instrs()

    next_leader = False
    for i in instrs:
        # After a jump
        if next_leader:
            next_leader = False
            i.set_leader()
        # This is a leader per-se
        if i.is_leader():
            leaders[id(i)] = i
        if i.has_blocks():
            for b in i.blocks():
                get_leaders(b[0], leaders)
        # We have a leader after a jump
        if i.is_jump():
            next_leader = True

def build_dot_string(blocks, links):
    """
    Constructs the input for DOT given a function representation.

        frepr - representation of function
        --
        returns: function representation
    """
    s = 'digraph{\n\tnode [shape=box];\n'
    for b in blocks.values():
        descr = b.description()
        if b.bid < 0:
            s += '\t%d [label="%s", style="filled", color="#f7007f"];\n' %\
                    (b.bid, descr)
        elif descr:
            s += '\t%d [label="%s"];\n' % (b.bid, descr)
        else:
            s += '\t%d [label="", shape="point"];\n' % b.bid

    for l in links:
        d = links[l]
        s += '\t%d -> %d' % l
        if d:
            if d[:5] == 'while':
                color = '#136136'
            elif d[:2] == 'if':
                color = '#ff7700'
            elif d[:4] == 'else':
                color = '#0077ff'
            else:
                color = '#c00fee'
            s += ' [label="%s", color="%s"]' % (fix(d), color)
        s += ';\n'

    return s + '}\n'

def get_inout_blocks(bid, links, ix):
    """
    Return blocks linked to block bid. ix gives the direction.
    """
    bs = []
    for l in links:
        if l[ix] == bid:
            bs.append(l[1 - ix])
    return bs

def get_in_blocks(bid, links):
    """
    Returns blocks with links to block with id bid.
    """
    return get_inout_blocks(bid, links, 1)

def get_out_blocks(bid, links):
    """
    Returns blocks linked to by block with id bid.
    """
    return get_inout_blocks(bid, links, 0)

def cleanup(blocks, links):
    """
    Removes useless empty nodes from the tree. They were used before to ensure
    proper construction of tree but not all of them are useful after the
    entire tree is build. Removes nodes with empty content.
    """
    change = True
    while change:
        to_del = []
        for b in blocks:
            if blocks[b].empty():
                outblocks = get_out_blocks(b, links)
                inblocks = get_in_blocks(b, links)
                if len(outblocks) < 2 and len(inblocks) < 2:
                    for ib in inblocks:
                        for ob in outblocks:
                            s = links[(ib, b)] + links[(b, ob)]
                            links[(ib, ob)] = s
                    to_del.append(b)
        for b in to_del:
            del blocks[b]
            outblocks = get_out_blocks(b, links)
            inblocks = get_in_blocks(b, links)
            for ib in inblocks:
                del links[(ib, b)]
            for ob in outblocks:
                del links[(b, ob)]
        change = to_del != []

def dot(fcts, opts):
    """
    Transform each function to the graphical representation.

        fcts - list of functions to transform
        opts - user options
        --
        returns: None
    """
    for fname, frepr in fcts:
        block = frepr.block()

        # get leaders
        leaders = {}
        get_leaders(block, leaders)

        # get BBs
        blocks = {START:ast.BB(START), END:ast.BB(END)}
        links = {}
#        blocks[START].set_istream(block, blocks, leaders, links)
        # first instruction block
        b = blocks[START].build_new_BB(blocks)
        b.set_istream2(blocks, leaders, links, block.instrs(), blocks[START],
                blocks[END], blocks[START], blocks[END])

#        cleanup(blocks, links)

        s = build_dot_string(blocks, links)

        if not os.path.exists(opts.outdir):
            os.system('mkdir %s' % opts.outdir)
        filename = '%s/%s.dot' % (opts.outdir, fname)
        with open(filename, 'w') as f:
            f.write(s)
        os.system('dot -Tpng %s > %s/%s.png' % (filename, opts.outdir, fname))

        Labellist = {}

        firstBB = ast.LabelInstruction('%s' % 'START').toBB(Labellist, ast.BB())
        lastBB = frepr.toBB(Labellist, firstBB)
        ast.LabelInstruction('%s' % 'END').toBB(Labellist, lastBB)
#        blocks[0].visit(DotVisitor())
        Labellist['END'].remove_links()

        link_labels(Labellist['START'], Labellist, [], None)
        Labellist['START'].visit(DotVisitor())


def link_labels(node, labels, viz, last_loop):
    viz.append(node)
    i = node.first_instr()
    if i and i.is_instr() and i.is_loop():
        last_loop = node
    for next_node in node.get_link_list():
        if next_node not in viz:
            link_labels(next_node, labels, viz, last_loop)

    if i and i.is_instr():
        if i.is_goto():
            node.remove_links()
            node.add_link(labels[i.label()])
        if i.is_return():
            node.remove_links()
            node.add_link(labels['END'])
        if i.is_continue():
            node.remove_links()
            node.add_link(last_loop)
        if i.is_break():
            last = labels[last_loop]
            node.remove_links()
            node.add_link(last)

class DotVisitor:

    def __init__(self):
        self.g = open('test.dot', 'w')
        self.g.write('digraph {\n')
        self.lvl = 0
        self.viz = []
        self.description = ''

    def __call__(self, node):
        self.viz.append(node)
        self.description += '\t%d [label=\"%s\"' % (node.bid, \
                fix('%s' % node.instrs()))
        if not node.instrs() or node.instrs()[0].is_point():
            self.description += ', shape=\"point\"'
        self.description += '];\n'

        for next_node in node.get_link_list():
            self.g.write('\t' + node.bid.__str__() + ' -> ' + \
                    next_node.bid.__str__() + ';\n')
            if next_node not in self.viz:
                self.lvl += 1
                self(next_node)
                self.lvl -= 1

        if  self.lvl == 0:
            self.g.write(self.description)
            self.g.write('}')
            self.g.close()

