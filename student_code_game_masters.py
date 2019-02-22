from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg1 = []
        peg2 = []
        peg3 = []
        for i in self.kb.facts:
            if i.statement.predicate == 'on':
                disk = i.statement.terms[0].term.element
                number = int(disk[-1:])
                if i.statement.terms[1].term.element == 'peg1':
                    peg1.append(number)
                if i.statement.terms[1].term.element == 'peg2':
                    peg2.append(number)
                if i.statement.terms[1].term.element == 'peg3':
                    peg3.append(number)
        peg1.sort()
        peg2.sort()
        peg3.sort()
        peg1 = tuple(peg1)
        peg2 = tuple(peg2)
        peg3 = tuple(peg3)
        return (peg1,peg2,peg3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if self.isMovableLegal(movable_statement):
            disk = movable_statement.terms[0].term.element
            peg1 = movable_statement.terms[1].term.element
            peg2 = movable_statement.terms[2].term.element
            #figure out disk below
            diskbelowques = parse_input('fact: (ontopof ' + disk + ' ?x)')
            listofbindings = self.kb.kb_ask(diskbelowques)
            #basic
            oldfact = parse_input('fact: (on ' + disk + ' ' + peg1 + ')')
            newfact = parse_input('fact: (on ' + disk + ' ' + peg2 + ')')
            #figure out if disk on where moving
            oldtopques = parse_input('fact: (top ?x ' + peg2 + ')')
            listofbindings2 = self.kb.kb_ask(oldtopques)
            self.kb.kb_retract(oldfact)
            self.kb.kb_assert(newfact)
            # empty rules
            oldempty = parse_input('fact: (empty ' + peg2 + ')')
            self.kb.kb_retract(oldempty)  # if wasn't empty just does nothing
            newempty = parse_input('fact: (empty ' + peg1 + ')')
            emptyques = parse_input('fact: (on ?x ' + peg1 + ')')
            listofbinding3 = self.kb.kb_ask(emptyques)
            if not listofbinding3:
                self.kb.kb_assert(newempty)
            #top rules
            if listofbindings2:
                oldtopdisk = listofbindings2[0].bindings[0].constant.element
                oldtop = parse_input('fact: (top ' + oldtopdisk + ' ' + peg2 + ')')
                self.kb.kb_retract(oldtop)
            movedtop = parse_input('fact: (top ' + disk + ' ' + peg1 + ')')
            self.kb.kb_retract(movedtop)
            movetop = parse_input('fact: (top ' + disk + ' ' + peg2 + ')')
            self.kb.kb_assert(movetop)
            if listofbindings:
                belowdisks = []
                for i in listofbindings:
                    belowdisks.append(i.bindings[0].constant.element)
                smallest = belowdisks[0]
                for i in belowdisks:
                    smallerques = parse_input('fact: (smaller ' + smallest + ' ' + i + ')')
                    listofbindings2 = self.kb.kb_ask(smallerques)
                    if not listofbindings2:
                        smallest = i
                staytop = parse_input('fact: (top ' + smallest + ' ' + peg1 + ')')
                self.kb.kb_assert(staytop)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        row1 = [0,0,0]
        row2 = [0,0,0]
        row3 = [0,0,0]
        for i in self.kb.facts:
            if i.statement.predicate == 'pos':
                tile = i.statement.terms[0].term.element
                number = tile[-1:]
                if number == 'y':
                    number = -1
                else:
                    number = int(number)
                col = i.statement.terms[1].term.element
                colnum = int(col[-1:])
                if i.statement.terms[2].term.element == 'pos1':
                    row1[colnum-1]=number
                if i.statement.terms[2].term.element == 'pos2':
                    row2[colnum - 1] = number
                if i.statement.terms[2].term.element == 'pos3':
                    row3[colnum - 1] = number
        row1 = tuple(row1)
        row2 = tuple(row2)
        row3 = tuple(row3)
        return (row1, row2, row3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if self.isMovableLegal(movable_statement):
            tile = movable_statement.terms[0].term.element
            col1 = movable_statement.terms[1].term.element
            row1 = movable_statement.terms[2].term.element
            col2 = movable_statement.terms[3].term.element
            row2 = movable_statement.terms[4].term.element
            oldfact = parse_input('fact: (pos ' + tile + ' ' + col1 + ' ' + row1 + ')')
            oldfact2 = parse_input('fact: (pos empty ' + col2 + ' ' + row2 + ')')
            newfact = parse_input('fact: (pos ' + tile + ' ' + col2 + ' ' + row2 + ')')
            newfact2 = parse_input('fact: (pos empty ' + col1 + ' ' + row1 + ')')
            self.kb.kb_retract(oldfact)
            self.kb.kb_retract(oldfact2)
            self.kb.kb_assert(newfact)
            self.kb.kb_assert(newfact2)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
