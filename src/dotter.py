# IxCode - app for code spelunking :: block diagram
# Transform functions to the corresponding block diagram

import os

import ast

def fix(string):
    """
    Escapes several entities form the passed in string to ensure proper DOT
    output.
    """
    string = string.replace('\\', '\\\\')
    string = string.replace('"', '\\"')
    return string

def link_labels(node, labels, viz, last_loop):
    """
    Link all the BB nodes to form a tree. take care of loops, gotos, breaks,
    continues, returns, etc. Recursive function. Takes care not to visit a
    node multiple times.
    """
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

def dot(fcts, opts):
    """
    Transform each function to the graphical representation.

        fcts - list of functions to transform
        opts - user options
        --
        returns: None
    """
    if not os.path.exists(opts.outdir):
        os.system('mkdir %s' % opts.outdir)

    for fname, frepr in fcts:
        filename = '%s/%s.dot' % (opts.outdir, fname)

        Labellist = {}
        firstBB = ast.LabelInstruction('%s' % 'START').toBB(Labellist, ast.BB())
        lastBB = frepr.toBB(Labellist, firstBB)
        ast.LabelInstruction('%s' % 'END').toBB(Labellist, lastBB)
        Labellist['END'].remove_links()

        link_labels(Labellist['START'], Labellist, [], None)
        Labellist['START'].visit(DotVisitor(filename))
        os.system('dot -Tpng %s > %s/%s.png' % (filename, opts.outdir, fname))

class DotVisitor:
    def __init__(self, filename):
        self.g = open(filename, 'w')
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
            self.g.write('}\n')
            self.g.close()

