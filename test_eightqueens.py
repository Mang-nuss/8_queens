# author: MJ
# 2019-12-11

import pytest
from eight_queens import Game

"""
TDD:
A number of test cases (commented out by: #) used for developing the functionalities needed
for solving the 8 queens exercise.
1. Red phase: implement a failing test
2. Green phase: write production code to pass the test
3. Refactor & unmark the test object
"""


# .....FIXTURES..........#

@pytest.fixture(autouse=True)  # Instantiaton
def g():
    print("started: g")
    game = Game(8)
    print("current Piece (g):", game.getCurrentPiece().getPieceId())
    return game  # the 'g' function is called for each test method


@pytest.fixture()  # Instantiaton
def p(g):
    print("started: p")
    piece = g.getCurrentPiece()
    print("current Piece (p):", piece.getPieceId())
    return piece


# .....TESTS.............#

# all pieces are there
def test_1(p,g):
    assert len(g.setOfPieces) == 8
    assert p.getPieceId() == 1


# all pieces have the correct positions on board
def test_2(p,g):
    assert p.getPieceId() == 1
    for i in range(len(g.setOfPieces)):
        p = g.pieceIsNow(i+1)
        assert p.getCurrentPosition() == [1,i+1]


# piece 1 is registered as threatening 7 row positions
def test_3(p,g):
    p = g.pieceIsNow(1)
    p.checkRow(8)
    assert len(p.threatensPositions) == 7


# these positions are the correct ones
def test_4(p,g):
    for i in range(len(g.setOfPieces)):
        p = g.pieceIsNow(i+1)
        assert p.getPieceId() == i+1


# piece 1 is registered as not threatening up left
def test_5(p,g):
    #p = g.pieceIsNow(1)
    assert p.getPieceId() == 1
    p.checkUpLeft()
    assert len(p.threatensPositions) == 0


# piece 1 is registered as not threatening up right
def test_6(p,g):
    p.checkUpRight(8)
    assert len(p.threatensPositions) == 0


# piece 1 is registered as not threatening down left
def test_7(p,g):
    p.checkDownLeft(8)
    assert len(p.threatensPositions) == 0


# piece 1 is registered as threatening down right
def test_8(p,g):
    p.checkDownRight(8)
    assert len(p.threatensPositions) == 7

# These control functions are refactored as registerThreatenedPositions


# the other pieces do not belong to the diagonal positions
def test_9(p,g):
    del p.threatensPositions[:8]
    for i in range(8):
        current = g.pieceIsNow(i)
        assert current.getCurrentPosition() not in p.threatensPositions


# all pieces are registered as threatening in the same way
def test_10(p,g):
    for i in range(2,8):
        p = g.pieceIsNow(i)
        p.registerThreatenedPositions(8)
        assert len(p.threatensPositions) == 14


# piece 1 takes next position
def test_11(p,g):
    p = g.pieceIsNow(1)
    g.move(p)
    assert p.getCurrentPosition() == [2,1]


# all other pieces have kept their positions
def test_12(p,g):
    for i in range(1,len(g.setOfPieces)):
        p = g.pieceIsNow(i+1)
        assert p.getCurrentPosition() == [1,i+1]


# piece 1 takes all positions in its column
def test_13(p,g):
    p = g.pieceIsNow(1)
    p.setCurrentPosition([1,1])
    i = p.getCurrentPosition()[0]
    while i < g.dimension:
        g.move(p)
        i += 1
    assert p.getCurrentPosition() == [8,1]


# on all positions, it is registered as threatening
def test_14(p,g):
    p.setCurrentPosition([1,1])
    i = p.getCurrentPosition()[0]
    while i < g.dimension:
        g.move(p)
        p.registerThreatenedPositions(g.dimension)
        assert p.getCurrentPosition() == [i+1,p.getPieceId()]
        i += 1

    assert g.isThreatening(p) == True

    """while i < g.dimension:
        g.move(p)
        assert g.pieceHasThreatenedPositions(p,g.dimension) == True
        #p.clearThreatensPositions()
        i += 1"""

# piece 1 is registered as threatening by correct reason
def test_15(p,g):
    p.setCurrentPosition([1,1])
    i = p.getCurrentPosition()[0]
    while i < g.dimension:
        g.move(p)
        p.registerThreatenedPositions(g.dimension)
        assert p.getCurrentPosition() == [i+1,p.getPieceId()]
        i += 1

    assert g.isThreatening(p) == True

    p = g.pieceIsNow(8)
    p.registerThreatenedPositions(g.dimension)
    assert p.getCurrentPosition() == [1,8]
    assert len(p.threatensPositions) == 14


def test_16(p,g):
    li = p.threatensPositions
    p = g.pieceIsNow(8)
    assert p.getCurrentPosition() not in li #does not threaten itself


# piece 1 is moved back to first position
def test_17(p,g):
    p = g.pieceIsNow(1)
    p.setCurrentPosition([1,p.getPieceId()])
    assert p.getCurrentPosition() == [1,1]


# piece 1 cannot be the first to be moved (and is listed as such)
def test_18(p,g):
    g.addToPiecesThatCannotBeMovedFirst(p.getPieceId())
    assert g.piecesThatCannotBeMovedFirst[0] == 1


# next piece (2) is picked
def test_19(p,g):
    p = g.pickNextPiece()
    assert p.getPieceId() == 2
    assert g.getCurrentPiece().getPieceId() == 2


# piece 2 is moved until it does not threaten
def test_20(p,g):
    p = g.pickNextPiece()
    assert p.getPieceId() == 2
    assert g.getCurrentPiece().getPieceId() == 2

    assert p.getPieceId() == 2
    for i in range(g.dimension-1):
        g.move(p)
        p.registerThreatenedPositions(g.dimension)

        threatening = g.isThreatening(p)
        if not threatening:
            break

    assert p.getCurrentPosition() == [8, 2]
    assert [1,8] not in p.threatensPositions
    assert threatening == False
    assert p.getPieceId() == 2


# piece 3 is moved until it does not threaten
def test_21(g,p):
    p = g.pieceIsNow(2)
    assert p.getPieceId() == 2
    g.positionsAreReset()
    p = g.pieceIsNow(3)

    for i in range(g.dimension-1):
        g.move(p)
        p.registerThreatenedPositions(g.dimension)

        if not g.isThreatening(p):
            break

    #piece = g.setOfPieces[2] #piece nr 3
    #assert piece.getPieceId() == 3
    #assert piece.getCurrentPosition() == [1,3]
    assert p.getCurrentPosition() == [7, 3]
    #assert [7,3] not in p.threatensPositions
    assert g.isThreatening(p) == False
    assert p.getPieceId() == 3


# piece 4 is moved until it does not threaten
def test_22(p,g):
    p = g.pickNextPiece()
    p = g.pickNextPiece()
    assert p.getPieceId() == 3
    g.positionsAreReset()
    p = g.pieceIsNow(4)

    for i in range(g.dimension):
        g.move(p)
        p.registerThreatenedPositions(g.dimension)

        if not g.isThreatening(p):
            break

    assert p.getPieceId() == 4
    #piece = g.setOfPieces[2] #piece nr 3
    #assert piece.getPieceId() == 3
    #assert piece.getCurrentPosition() == [1,3]
    assert p.getCurrentPosition() == [6, 4]
    assert g.isThreatening(p) == False
    assert p.getPieceId() == 4 #isThreatening does not switch current piece.


# board is pictured
def test_23(p,g):
    p = g.pickNextPiece()
    p = g.pickNextPiece()
    assert p.getPieceId() == 3
    g.positionsAreReset()
    p = g.pieceIsNow(4)

    for i in range(g.dimension):
        g.move(p)
        p.registerThreatenedPositions(g.dimension)

        if not g.isThreatening(p):
            break

    assert p.getPieceId() == 4
    assert p.getCurrentPosition() == [6, 4]
    assert g.isThreatening(p) == False
    assert p.getPieceId() == 4 #isThreatening does not switch current piece.
    assert p.getCurrentPosition() == [6, 4]
    assert p.getPieceId() == 4
    g.pictureBoard()
    #assert g.getPieceId() == 8


# all remaining pieces are moved in the same way
def test_24(p,g):
    for n in range(len(g.setOfPieces)):
        p = g.pieceIsNow(n+1)
        #x_spot = p.getCurrentPosition()[0]
        for i in range(g.dimension-1):
            g.move(p)
        assert p.getCurrentPosition()[0] == 8
    g.pictureBoard()

# method for deciding whether or not piece can be moved first
def test_25(p,g):
    g.piecesMovedInRound.append(p.getPieceId())
    for i in range(g.dimension-1):
        g.move(p)
        p.registerThreatenedPositions(g.dimension)
    if g.isThreatening(p):
        p.cannotBeMoved = True
        g.checkIfPieceCanBeMovedFirst(p)
    assert p.cannotBeMovedFirst == True
    g.pictureBoard()

"""

- piece 1 is registered as threatened by correct reason
- piece 1 is moved back to first position
- piece 1 cannot be the first to be moved (and is listed as such)
- next piece (2) is picked
- piece 2 is moved until it is not threatened
- piece 2 is registered as not threatened
- piece 2 is registered as moved
- piece 2 is now moved. piece 3 tries out every spot, unsuccessfully.
-
- all remaining pieces are moved in the same way
- check if fulfilled
- if not, the first threatened piece (that can be the first to be moved) is again picked 
    (it may be the same piece as before)
- when moved, piece is registered as moved
- if a piece is to be tried out a 2nd time since last registered move, game is over
- the piece that was moved first

"""
