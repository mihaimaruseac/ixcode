# IxCode - app for code spelunking :: block diagram
# Generic AST.

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
    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        return "-->" + self.__str__() + "<--"

class Block(Node):
    """
    A block of several instructions.
    """
    __bid = -100
    def __init__(self, auto_assign_id=False):
        self._instructions = []
        self._bid = 0
        self._aaid = auto_assign_id
        if self._aaid:
            self._bid = Block.__bid
            Block.__bid -= 1

    def add(self, i):
        if i:
            if not self._instructions:
                if not self._aaid:
                    self._bid = id(i)
                i.set_leader()
            self._instructions.append(i)

    def instrs(self):
        return self._instructions

    def get_bb_id(self):
        return self._bid

    def __str__(self):
        return "<block> {...}"

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

    def __str__(self):
        return self._text

    def name(self):
        return self._name

    def block(self):
        if self._block.is_block():
            return self._block.block()
        return self._block

class TextNode(Node):
    """
    A node containing a text describing the corresponding instruction.
    """
    def __init__(self, text):
        self._text = text

    def __str__(self):
        return self._text

class Expression(TextNode):
    """
    A simple expression, a subpart of an instruction.
    """
    pass

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

    def is_block(self):
        """
        Returns True if this is a block.
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
        return False

    def is_goto(self):
        return False

    def is_label(self):
        return False

    def pass_through(self):
        return False

    def insides(self, links):
        """
        Returns inside blocks to jump there if any or [].
        """
        return []

class RetInstruction(Instruction):
    """
    A return instruction. Always in a single block.
    """
    def __init__(self, text):
        Instruction.__init__(self, text)
        self._leader = True

    def is_return(self):
        return True

class ForInstruction(Instruction):
    """
    A for instruction. Causes a jump.
    """
    def __init__(self, header, content):
        Instruction.__init__(self, "for %s {...}" % header)
        self._header = header
        if not content.is_block():
            self._content = Block()
            self._content.add(content)
        else:
            self._content = content.block().block()

    def is_block(self):
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

    def insides(self, links):
        bid = self._content.get_bb_id()
        links[(bid, bid)] = 'for %s' % self._header
        js = [(bid, '')]
        return js

class MacroLoopInstruction(ForInstruction):
    """
    A macro which represents a loop. Guessed.
    """
    def __init__(self, header, content):
        ForInstruction.__init__(self, "#loop %s" % header, content)

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

    def is_jump(self):
        return True

    def is_goto(self):
        return True

    def label(self):
        return self._label

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
        return '%s' % self._label

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

    def is_jump(self):
        return True

class IfInstruction(Instruction):
    """
    An if. Will always create two blocks.
    """
    def __init__(self, cond, true, false):
        Instruction.__init__(self, "if (%s){...}" % cond)
        self._cond = cond

        if not true.is_block():
            self._true = Block()
            self._true.add(true)
        else:
            self._true = true.block().block()
        if not false:
            self._false = Block(auto_assign_id=True)
        elif not false.is_block():
            self._false = Block()
            self._false.add(false)
        else:
            self._false = false.block().block()

    def is_jump(self):
        return True

    def is_block(self):
        return True

    def blocks(self):
        return [(self._true, 'if %s' % self._cond), (self._false, 'else')]

    def insides(self, links):
        bid_true = self._true.get_bb_id()
        bid_false = self._false.get_bb_id()
        js = [(bid_true, 'if %s' % self._cond), (bid_false, 'else')]
        return js

