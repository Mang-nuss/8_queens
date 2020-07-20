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
    game = Game(8)
    return game  # the 'g' function is called for each test method


@pytest.fixture()  # Instantiaton
def p(g):
    piece = g.getCurrentPiece()
    return piece


# .....TESTS.............#

# all pieces are there
def test_1(g):
    assert len(g.setOfPieces) == 8


# all pieces have the correct positions on board
def test_2(p,g):
    for i in range(len(g.setOfPieces)):
        p = g.pieceIsNow(i+1)
        assert p.getCurrentPosition() == [1,i+1]


# piece 1 is registered as threatened by 7 row positions
def test_3(p,g):
    p = g.pieceIsNow(1)
    p.checkRow(8)
    assert len(p.threatensPositions) == 8


# these positions are the correct ones
def test_4(p,g):
    for i in range(len(g.setOfPieces)):
        p = g.pieceIsNow(i+1)
        assert p.getPieceId() == i+1


# piece 1 is registered as not threatened from up left
def test_5(p,g):
    p = g.pieceIsNow(1)
    p.checkUpLeft()
    assert len(p.threatensPositions) == 8


# piece 1 is registered as not threatened from up right
def test_6(p,g):
    p.checkUpRight(8)
    assert len(p.threatensPositions) == 8


# piece 1 is registered as not threatened from down left
def test_7(p,g):
    p.checkDownLeft(8)
    assert len(p.threatensPositions) == 8


# piece 1 is registered as threatened from down right
def test_8(p,g):
    p.checkDownRight(8)
    assert len(p.threatensPositions) == 15


# the other pieces do not belong to the diagonal positions
def test_9(p,g):
    del p.threatensPositions[:8]
    for i in range(8):
        current = g.pieceIsNow(i)
        assert current.getCurrentPosition() not in p.threatensPositions


# all pieces are registered as threatened in the same way
def test_10(p,g):
    for i in range(2,8):
        p = g.pieceIsNow(i)
        p.registerThreatenedPositions(8)
        assert len(p.threatensPositions) == 15


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


# on all positions, it is registered as threatened
def test_14(p,g):
    p.setCurrentPosition([1,1])
    i = p.getCurrentPosition()[0]
    while i < g.dimension:
        g.move(p)
        assert g.pieceHasThreatenedPositions(p,g.dimension) == True
        #p.clearThreatensPositions()
        i += 1


"""

- all other pieces have kept their positions
- piece 1 takes all positions in its column
- on all positions, it is registered as threatened
- piece 1 is registered as threatened by correct reason
- piece 1 is moved back to first position
- piece 1 cannot be the first to be moved (and is listed as such)
- next piece (2) is picked
- piece 2 is moved until it is not threatened
- piece 2 is registered as not threatened
- piece 2 is registered as moved
- all remaining pieces are moved in the same way
- check if fulfilled
- if not, the first threatened piece (that can be the first to be moved) is again picked 
    (it may be the same piece as before)
- when moved, piece is registered as moved
- if a piece is to be tried out a 2nd time since last registered move, game is over.

"""
