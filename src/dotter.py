# IxCode - app for code spelunking :: block diagram
# Transform functions to the corresponding block diagram

import os

START = -1
END = -2

class BB:
    """
    A basic block. To be displayed by itself in the diagram.
    """
    __bid__ = 0
    def __init__(self, bid = 0):
        if bid < 0:
            self.bid = bid
        else:
            self.bid = BB.__bid__
            BB.__bid__ += 1
        self._leader = None
        self._instrs = []

    def labeled(self, label):
        if self._leader and self._leader.is_label() and \
           self._leader.label() == label:
            return True
        return False

    def build_new_BB(self, blocks):
        new_block = BB()
        blocks[new_block.bid] = new_block
        return new_block

    def set_istream(self, block, blocks, leaders, links, visited=[],
            unsolved_jumps={}):
        """
        Receives the instruction stream and returns the entire Basic Block
        hierarchy using the passed-in dictionaries and lists.

        Basically, if we are the starting node recourse with the same
        instruction stream, collect the last node and link it to the exit
        point.

        Otherwise, check each instruction in stream and either add it to the
        current block or create another. When creating another either switch
        to a new instruction stream (the instruction was a block) or use the
        same (the instruction caused a break in block flow).

        Create virtual nodes in several places to ensure all links are ok. For
        example, if not using this the if would have three outbound nodes, but
        it really has two.

        This method may contain several bugs, they will be discovered through
        testing. It is the hardest part of this program.
        """
        if self.bid == START:
            new_block = self.build_new_BB(blocks)
            links[(self.bid, new_block.bid)] = ''
            last_blocks = new_block.set_istream(block, blocks, leaders, links,
                    visited, unsolved_jumps)
            for b in last_blocks:
                links[(b.bid, END)] = ''
            for bid in unsolved_jumps:
                label = unsolved_jumps[bid]
                for b in blocks:
                    if blocks[b].labeled(label):
                        links[bid, b] = ''
            return []

        instrs = block.instrs()

        break_stream_block = None
        for i in instrs:
            if i in visited:
                continue
            visited.append(i)

            if i.is_block():
                subblocks = []
                for b, t in i.blocks():
                    new_block = self.build_new_BB(blocks)
                    if i.is_loop():
                        links[(new_block.bid, new_block.bid)] = i.loop_label()
                    links[(self.bid, new_block.bid)] = t
                    subblocks.extend(new_block.set_istream(b, blocks,
                        leaders, links, visited, unsolved_jumps))
                new_block = self.build_new_BB(blocks)
                for b in subblocks:
                    links[(b.bid, new_block.bid)] = ''
                if i.pass_through():
                    links[(self.bid, new_block.bid)] = ''
                return new_block.set_istream(block, blocks, leaders, links,
                        visited, unsolved_jumps)
            else:
                if i.is_leader():
                    if not self._leader:
                        self._leader = i
                    else:
                        # time for a new block
                        new_block = self.build_new_BB(blocks)
                        last = self._instrs[-1]
                        if not last.is_goto():
                            links[(self.bid, new_block.bid)] = ''
                        else:
                            unsolved_jumps[self.bid] = last.label()
                        subblocks = new_block.set_istream(block, blocks,
                                leaders, links, visited[:-1], unsolved_jumps)
                        new_block = self.build_new_BB(blocks)
                        for b in subblocks:
                            links[(b.bid, new_block.bid)] = ''
                        return [new_block]
                self._instrs.append(i)

        if not self._instrs:
            return [self]

        last = self._instrs[-1]
        if not last.is_goto():
            return [self]
        unsolved_jumps[self.bid] = last.label()
        return []

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

    def empty(self):
        return self._instrs == [] and self.bid >= 0

    def instrs(self):
        return self._instrs

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
            for b in i.blocks():
                get_leaders(b[0], leaders)
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
        if descr:
            s += '\t%d [label="%s"];\n' % (b.bid, descr)
        else:
            s += '\t%d [label="", shape="point"];\n' % b.bid

    for l in links:
        d = links[l]
        s += '\t%d -> %d' % l
        if d:
            s += ' [label="%s"]' % d
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
    to_del = []
    for b in blocks:
        if blocks[b].empty():
            outblocks = get_out_blocks(b, links)
            if len(outblocks) == 1: # if otherwise we should (maybe?) raise an error
                inblocks = get_in_blocks(b, links)
                for ib in inblocks:
                    s = links[(ib, b)] + links[(b, outblocks[0])]
                    del links[(ib, b)]
                    del links[(b, outblocks[0])]
                    links[(ib, outblocks[0])] = s
                to_del.append(b)
    for d in to_del:
        del blocks[d]

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
        blocks = {START:BB(START), END:BB(END)}
        links = {}
        blocks[START].set_istream(block, blocks, leaders, links)

        # cleanup tree
        cleanup(blocks, links)

        s = build_dot_string(blocks, links)

        if not os.path.exists(opts.outdir):
            os.system('mkdir %s' % opts.outdir)
        filename = '%s/%s.dot' % (opts.outdir, fname)
        with open(filename, 'w') as f:
            f.write(s)
        os.system('dot -Tpng %s > %s/%s.png' % (filename, opts.outdir, fname))

