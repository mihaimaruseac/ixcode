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
                        links[bid, b] = 'jmp'
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
                    links[(b.bid, new_block.bid)] = 'l'
                if i.pass_through():
                    links[(self.bid, new_block.bid)] = 'p'
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
                            links[(b.bid, new_block.bid)] = 'v'
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

def get_blocks(block, leaders, blocks):
    instrs = block.instrs()

    last_leader = None
    bbi = []
    for i in instrs:
        if id(i) in leaders:
            if last_leader:
                b = BB(id(last_leader), last_leader, bbi)
                blocks[b.bid] = b
                bbi = []
            last_leader = i
        if i.is_block():
            for b in i.blocks():
               get_blocks(b, leaders, blocks)
        else:
            bbi.append(i)
    if last_leader:
        b = BB(id(last_leader), last_leader, bbi)
        blocks[b.bid] = b
    else:
        b = BB(block.get_bb_id(), None, instrs)
        blocks[block.get_bb_id()] = b

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
        blocks = {START:BB(START), END:BB(END)}
        links = {}
        blocks[START].set_istream(block, blocks, leaders, links)

        s = build_dot_string(blocks, links)

        filename = '%s.dot' % fname
        with open(filename, 'w') as f:
            f.write(s)
        os.system('dot -Tpng %s > %s.png' % (filename, fname))

