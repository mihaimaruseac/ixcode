# IxCode - app for code spelunking :: block diagram
# Generic AST.

from dotter import BB

START = -1
END = -2

#def find(cBB):
#    if(cBB._instrs()):
#        if(cBB._instrs[0].is_loop()):
#            return cBB
#    else:
#        for i in cBB._lin:
#            find(i)


class File():
    """
    A file. Contains the list of functions.
    """
    def __init__(self):
        self._fcts = {}

    def add(self, f):
        if f:
            self._fcts['%s' % f.name()] = f

    def filter(self, functions=[]):
        """
        Filters the ast to contain only interesting functions. If functions = []
        no filtering is done.
        """
        if functions:
            d = {}
            for f in functions:
                d[f] = self._fcts[f]
            self._fcts = d

    def visit(self, visitor):
        raise NotImplementedError('%s' % self.__class__)

    def toBB(self, BBlabels, cBB):
        raise NotImplementedError('%s' % self.__class__)

    def __iter__(self):
        """
        Returns the stored functions, one by one.
        """
        for f in self._fcts:
            yield (f, self._fcts[f])

    def __str__(self):
        return 'File: %s' % self._fcts

    def __repr__(self):
        return "-->" + self.__str__() + "<--"

class Node:
    """
    Base class for all nodes in AST. All methods raise exceptions to ensure
    proper derivation.
    """

    def __init__(self, info = None):
        self.info = info

    def visit(self, visitor):
        return visitor(self)

    def toBB(self, Labellist, cBB):
        raise NotImplementedError('%s' % self.__class__)

    def __str__(self):
        return self.info.__str__()

    def __repr__(self):
        return "-->" + self.__str__() + "<--"

class Block(Node):
    """
    A block of several instructions.
    """
    def __init__(self):
        self._instructions = []

    def add(self, i):
        if i:
            if not self._instructions:
                i.set_leader()
            self._instructions.append(i)

    def instrs(self):
        return self._instructions

    def toBB(self, Labellist, cBB):
        lastBB = cBB
        for i in self._instructions:
            if lastBB.is_ignored():
                return lastBB
            lastBB = i.toBB(Labellist, lastBB)
        return lastBB

    def __str__(self):
        return "<block> {...}"

    def visit(self, visitor):
        ret = None
        for i in self._instructions:
            ret = i.visit(visitor)
        return ret

class Function(Node):
    """
    A function.
    """
    def __init__(self, name, header, arg, block):
        """
        name    -   name of function
        header  -   declaration (inline int from inline int f(int a, int b))
        arg     -   arguments (int a, int b from above decl)
        block   -   content
        """
        self._text = '%s %s(%s){...}' % (header, name, arg)
        self._name = name
        self._block = block

    def name(self):
        return self._name

    def block(self):
        if self._block.is_block():
            return self._block.block()
        return self._block

    def visit(self, visitor):
        return self._block.visit(visitor)

    def toBB(self, Labellist, cBB):
        return self._block.toBB(Labellist, cBB)

    def __str__(self):
        return self._text

class TextNode(Node):
    """
    A node containing a text describing the corresponding instruction.
    """

    def __init__(self, text):
        self._text = text

    def is_instr(self):
        return False

    def is_point(self):
        return False

    def toBB(self, Labellist, cBB):
        if not cBB:
            cBB = BB()
        if cBB.instrs():
            newBB = BB()
            newBB.add_instruction(self)
            cBB.add_link(newBB)
            return newBB
        cBB.add_instruction(self)
        return cBB

    def __init__(self, text):
        self._text = text

    def get_text(self):
        return self._text

    def __str__(self):
        return self._text

class Expression(TextNode):
    """
    A simple expression, a subpart of an instruction. A TextNode for all
    purposes of this program.
    """
    pass

class Point(TextNode):
    """
    A node to be displayed as a simple dot in the diagram.
    """
    def is_point(self):
        return True

class Instruction(TextNode):
    """
    An instruction to be displayed in the diagram. Doesn't jump.
    """
    def __init__(self, text):
        TextNode.__init__(self, text)
        self._leader = False

    def set_leader(self):
        if not self.is_block():
            self._leader = True

    def is_leader(self):
        """
        Returns True if this instruction leads a basic block.
        """
        return self._leader

    def is_instr(self):
        return True

    def is_block(self):
        """
        Returns True if this is a block of instructions.
        """
        return False

    def has_blocks(self):
        """
        Returns True if this instruction contains blocks of other
        instructions. If True, they can be accessed via blocks().
        """
        return False

    def is_jump(self):
        """
        Returns True if this instruction may jump.
        """
        return False

    def is_loop(self):
        """
        Returns True if this is a loop.
        """
        return False

    def is_return(self):
        """
        True if this is a return instruction.
        """
        return False

    def is_goto(self):
        """
        True if this is a goto instruction.
        """
        return False

    def is_label(self):
        """
        True if this is a label instruction.
        """
        return False

    def pass_through(self):
        """
        True if this block can be skipped.
        """
        return False

    def has_subblock(self):
        """
        True if this instruction contains a block (it is an if, while,
        do..while or for).
        """
        return False

    def link_blocks(self, header, exit, links):
        """
        Links the internal blocks with the header and the exit one, updates
        the link dictionary.
        """
        pass

    def is_break(self):
        """
        True if this is a break instruction.
        """
        return False

    def is_continue(self):
        """
        True if this is a continue instruction.
        """
        return False

    def visit(self, visitor):
        visitor(self)

    def toBB(self, Labellist, cBB):
        if not cBB:
            cBB = BB()

        if not self.is_leader() or not cBB.instrs():
            cBB.add_instruction(self)
            return cBB

        newBB = BB();
        newBB.add_instruction(self)
        cBB.add_link(newBB)
        return newBB

class BreakInstruction(Instruction):
    """
    A break instruction.
    """
    def __init__(self):
        Instruction.__init__(self, 'break')

    def is_break(self):
        return True

    def toBB(self, Labellist, cBB):
        cBB = (Instruction).toBB(self, Labellist, cBB)
        lastBB = BB()
        cBB.add_link(lastBB)
        return lastBB

class ContinueInstruction(Instruction):
    """
    A continue instruction.
    """
    def __init__(self):
        Instruction.__init__(self, 'continue')

    def is_continue(self):
        return True

    def toBB(self, Labellist, cBB):
        cBB = (Instruction).toBB(self, Labellist, cBB)
        lastBB = BB()
        cBB.add_link(lastBB)
        return lastBB

class RetInstruction(Instruction):
    """
    A return instruction. Always in a single block.
    """
    def __init__(self, text):
        Instruction.__init__(self, text)
        self._leader = True

    def is_return(self):
        return True

    def toBB(self, Labellist, cBB):
        cBB = Instruction.toBB(self, Labellist, cBB)
        lastBB = BB()
        cBB.add_link(lastBB)
        return lastBB

class ForInstruction(Instruction):
    """
    A for instruction. Causes a jump.
    """
    def __init__(self, header, content):
        Instruction.__init__(self, "for %s {...}" % header)
        self._header = header
        self._leader = True
        if not content.is_block():
            self._content = Block()
            self._content.add(content)
        else:
            self._content = content.block().block()

    def has_blocks(self):
        return True

    def is_jump(self):
        return True

    def is_loop(self):
        return True

    def blocks(self):
        return [(self._content, '')]

    def loop_label(self):
        return 'for %s' % self._header

    def pass_through(self):
        return True

    def has_subblock(self):
        return True

    def subblocks(self):
        return [(self._content, '')]

    def link_blocks(self, header, exit, links):
        links[(header.bid, exit.bid)] = 'else'
        links[(exit.bid, header.bid)] = 'for %s' % self._header

    def visit(self, visitor):
        visitor(self)
        self._content.visit(visitor)

    def toBB(self, Labellist, cBB):
        firstBB = Instruction.toBB(self, Labellist, cBB)
        lastBB = self._content.toBB(Labellist, firstBB)
        newBB = Point('%s' % '_POINT_').toBB(Labellist, lastBB)
        newBB.add_link(firstBB)
        firstBB.add_link(newBB)
        Labellist[firstBB] = newBB
        return newBB

class MacroLoopInstruction(ForInstruction):
    """
    A macro which represents a loop. Guessed. Otherwise, a simple for
    """
    def __init__(self, header, content):
        ForInstruction.__init__(self, "#loop %s" % header, content)
        self._header = header

    def loop_label(self):
        return '%s' % self._header

    def link_blocks(self, header, exit, links):
        links[(header.bid, exit.bid)] = 'else'
        links[(exit.bid, header.bid)] = '%s' % self._header

 #   def toBB(self, BBlabels, cBB):
  #      raise NotImplementedError('%s' % self.__class__)

class WhileInstruction(Instruction):
    """
    A while instruction. Causes a jump.
    """
    def __init__(self, header, content):
        Instruction.__init__(self, "while (%s) {...}" % header)
        self._header = header
        self._leader = True
        if not content.is_block():
            self._content = Block()
            self._content.add(content)
        else:
            self._content = content.block().block()

    def has_blocks(self):
        return True

    def is_jump(self):
        return True

    def is_loop(self):
        return True

    def blocks(self):
        return [(self._content, '')]

    def loop_label(self):
        return 'while (%s)' % self._header

    def pass_through(self):
        return True

    def has_subblock(self):
        return True

    def subblocks(self):
        return [(self._content, '')]

    def link_blocks(self, header, exit, links):
        links[(header.bid, exit.bid)] = 'else'
        links[(exit.bid, header.bid)] = 'while %s' % self._header

    def visit(self, visitor):
        visitor(self)
        self._content.visit(visitor)

    def toBB(self, Labellist, cBB):
        firstBB = Instruction.toBB(self, Labellist, cBB)
        lastBB = self._content.toBB(Labellist, firstBB)

        newBB = Point('%s' % '_POINT_').toBB(Labellist, lastBB)
        newBB.add_link(firstBB)
        firstBB.add_link(newBB)
        Labellist[firstBB] = newBB

        return newBB

class DoWhileInstruction(WhileInstruction):
    """
    A do...while instruction. A while but with no pass_through.
    """
    def __init__(self, header, content):
        WhileInstruction.__init__(self, "do {...} while (%s)" % header, content)
        self._header = header
        self._leader = True

    def pass_through(self):
        return False

    def link_blocks(self, header, exit, links):
        # No else label :)
        links[(exit.bid, header.bid)] = 'do ... while %s' % self._header

    def toBB(self, Labellist, cBB):
        firstBB = Instruction.toBB(self, Labellist, cBB)
        lastBB = self._content.toBB(Labellist, firstBB)
        newBB = Expression('while (%s)' % self._header).toBB(Labellist, lastBB)
        newBB.add_link(firstBB)
        Labellist[firstBB] = newBB
        return newBB

class GoToInstruction(Instruction):
    """
    A goto instruction. Causes a jump.
    """
    def __init__(self, label):
        """
        label - where to jump
        """
        Instruction.__init__(self, "goto %s;" % label)
        self._label = label
        self._leader = True

    def is_jump(self):
        return True

    def is_goto(self):
        return True

    def label(self):
        """
        Returns label to jump to.
        """
        return self._label

    def toBB(self, Labellist, cBB):
        cBB = Instruction.toBB(self, Labellist, cBB)
        lastBB = BB()
        cBB.add_link(lastBB)
        return lastBB

class LabelInstruction(Instruction):
    """
    A label. Always the start of a new block.
    """
    def __init__(self, label):
        """
        label - text of label
        """
        Instruction.__init__(self, "%s:" % label)
        self._label = label
        self._leader = True

    def is_label(self):
        return True

    def label(self):
        """
        Returns label text.
        """
        return '%s' % self._label

    def toBB(self, Labellist, cBB):
        cBB = Instruction.toBB(self, Labellist, cBB)
        lastBB = BB()
        cBB.add_link(lastBB)
        Labellist['%s' % self._label] = cBB
        return lastBB

class BlockInstruction(Instruction):
    """
    A {...} block. Always a new block.
    """
    def __init__(self, block):
        Instruction.__init__(self, "{...}")
        self._block = block

    def block(self):
        return self._block

    def is_block(self):
        return True

    def has_blocks(self):
        return True

    def blocks(self):
        return [(self._block, '')]

    def is_jump(self):
        return True

    def visit(self, visitor):
        return self._block.visit(visitor)

    def toBB(self, Labellist, cBB):
        return self._block.toBB(Labellist, cBB)

class IfInstruction(Instruction):
    """
    An if. Will always create two blocks.
    """
    def __init__(self, cond, true, false):
        Instruction.__init__(self, "if (%s){...}" % cond)
        self._cond = cond
        self._leader = True

        if not true.is_block():
            self._true = Block()
            self._true.add(true)
        else:
            self._true = true.block().block()
        if not false:
            self._false = Block()
        elif not false.is_block():
            self._false = Block()
            self._false.add(false)
        else:
            self._false = false.block().block()

    def is_jump(self):
        return True

    def has_blocks(self):
        return True

    def blocks(self):
        return [(self._true, 'if %s' % self._cond), (self._false, 'else')]

    def has_subblock(self):
        return True

    def subblocks(self):
        return [(self._true, 'if %s' % self._cond), (self._false, 'else')]

    def visit(self, visitor):
        visitor(self)
        self._true.visit(visitor)
        self._false.visit(visitor)

    def toBB(self, Labellist, cBB):
        firstBB = Instruction.toBB(self, Labellist, cBB)
        lastBB = BB()

        if self._true:
            newBB = self._true.toBB(Labellist, firstBB)
            newBB.add_link(lastBB)

        if self._false:
            newBB = self._false.toBB(Labellist, firstBB)
            newBB.add_link(lastBB)
        else:
            firstBB.add_link(lastBB)

        return lastBB

