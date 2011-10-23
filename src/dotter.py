# IxCode - app for code spelunking :: block diagram
# Transform functions to the corresponding block diagram

import os

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

    def build_new_BB(klass, blocks):
        new_block = BB()
        blocks[new_block.bid] = new_block
        return new_block

    def labeled(self, label):
        if self._leader and self._leader.is_label() and \
           self._leader.label() == label:
            return True
        return False

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

            if i.has_blocks():
                subblocks = []
                for b, t in i.blocks():
                    new_block = self.build_new_BB(blocks)
                    links[(self.bid, new_block.bid)] = t
                    nbs = new_block.set_istream(b, blocks,
                        leaders, links, visited, unsolved_jumps)
                    subblocks.extend(nbs)
                    if i.is_loop():
                        for b in nbs:
                            links[(b.bid, new_block.bid)] = i.loop_label()
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
                        if i.is_return():
                            links[(self.bid, END)] = ''
                            self._instrs.append(i)
                            new_block = self.build_new_BB(blocks)
                            subblocks = new_block.set_istream(block, blocks,
                                    leaders, links, visited, unsolved_jumps)
                            new_block = self.build_new_BB(blocks)
                            for b in subblocks:
                                links[(b.bid, new_block.bid)] = ''
                            return [new_block]
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
        if last.is_return():
            links[(self.bid, END)] = ''
            return []
        if not last.is_goto():
            return [self]
        unsolved_jumps[self.bid] = last.label()
        return []

    def set_istream2(self, blocks, leaders, links, instrs, header, exit,
                    pheader, pexit, label='', defined_labels={},
                    undefined_jumps={}):
        """
        Receives a list of instructions and adds them to the block tree. Each
        block added is inserted into blocks with links in links. The leaders
        list is used to detect splits. also, new blocks can be created by some
        instructions like if, while, for, return, goto.

        The header and the exit blocks are the blocks before and after the
        current one. If header is None there was a goto before this block.

        Returns True if the current block has a normal link with the block
        following it.

        i.is_leader() == i in leaders.values() foreach i in instrs
        """
        if header:
           links[(header.bid, self.bid)] = label
        lastb = self
        # get instruction iterator
        leader_seen = False
        exit_following = True
        for i in instrs:
            assert i.is_leader() == (i in leaders.values())
            if i.is_leader():
                if leader_seen:
                    nb = self.build_new_BB(blocks)
                    if not exit_following:
                        lastb = None
                    istr = instrs[instrs.index(i):]
                    return nb.set_istream2(blocks, leaders, links, istr,
                            lastb, exit, pheader, pexit,
                            defined_labels=defined_labels,
                            undefined_jumps=undefined_jumps)
                leader_seen = True
            if i.has_subblock():
                h = self.build_new_BB(blocks)
                links[(self.bid, h.bid)] = '+'
                e = self.build_new_BB(blocks)
                lastb = e
                link_to_end = []
                new_blocks = []
                for sb, lbl in i.subblocks():
                    nb = self.build_new_BB(blocks)
                    new_blocks.append(nb)
                    if nb.set_istream2(blocks, leaders, links, sb.instrs(),
                            h, e, pheader, pexit, label=lbl,
                            defined_labels=defined_labels,
                            undefined_jumps=undefined_jumps):
                        link_to_end.append(nb)
                i.link_blocks(h, e, links)
                continue
            if i.is_label():
                l = i.label()
                defined_labels[l] = self.bid
                if undefined_jumps.has_key(l):
                    for b in undefined_jumps[l]:
                        links[(b, self.bid)] = '@'
                    del undefined_jumps[l]
                continue
            if i.is_goto():
                l = i.label()
                if defined_labels.has_key(l):
                    links[(lastb.bid, defined_labels[l])] = '-'
                else:
                    if undefined_jumps.has_key(l):
                        undefined_jumps[l].append(self.bid)
                    else:
                        undefined_jumps[l] = [self.bid]
                exit_following = False
                continue
            if i.is_break():
                links[(lastb.bid, pexit.bid)] = '#'
                continue
            self._instrs.append(i)
            if i.is_return():
                links[(self.bid, END)] = 'R'
                return False
        if exit_following:
            links[(lastb.bid, exit.bid)] = '>'
            return True
        return False # TODO: really?

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
            s += '%s\\n' % fix('%s' % i)
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
        blocks = {START:BB(START), END:BB(END)}
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

