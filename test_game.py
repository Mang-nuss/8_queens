import pytest
from game import Game


# .....FIXTURES..........#

@pytest.fixture(autouse=True)  # Instantiaton
def g():
    print("started: g")
    g = Game()
    return g


# .....TESTS.............#

# all pieces are there
def test_1(g):
    g.pictureBoard()
    assert True


# piece 1 is moved
def test_2(g):
    g.move()
    assert isinstance(g.currentPiece, int)
    assert g.currentPiece == 1
    assert isinstance(g.standing[g.currentPiece - 1], list)
    assert g.standing[g.currentPiece - 1] == [2, 1]
    assert g.checkRow() == False #added due to issues with test 11
    g.pictureBoard()


# piece 2 is moved once, 1 remaining at its new pos
def test_3(g):
    g.move()
    g.currentPiece += 1
    g.move()
    assert g.currentPiece == 2
    assert g.standing[g.currentPiece - 1] == [2, 2]
    assert g.standing[g.currentPiece - 2] == [2, 1]
    g.pictureBoard()


# neither is threatened from up left or down left
def test_4(g):
    g.move()
    g.currentPiece += 1
    g.move()
    assert g.checkUpLeft() == False
    g.currentPiece -= 1
    assert g.checkUpLeft() == False
    g.pictureBoard()


# the moves are counted correctly
def test_5(g):
    g.move()
    g.currentPiece += 1
    g.move()
    assert g.nrOfMoves == 2


# piece 2 is moved and is now threatened from up left
def test_6(g):
    g.move()
    g.currentPiece += 1
    g.move()
    g.move()
    assert g.checkUpLeft() == True


# piece 3 is threatened row-wise
def test_7(g):
    g.currentPiece += 2
    assert g.currentPiece == 3
    assert g.checkRow() == True
    assert g.isThreatened() == True


# piece 2  is moved until it is not threatened
def test_8(g):
    g.move()
    g.currentPiece += 1
    g.moveUntilUnthreatened()

    assert g.currentPiece == 2
    assert g.standing[g.currentPiece - 1] == [8, 2]


# next piece moves until unthreatened, if possible
def test_9(g):
    g.move()
    g.currentPiece += 1
    g.moveUntilUnthreatened()
    g.currentPiece += 1
    g.moveUntilUnthreatened()

    assert g.isThreatened() == True
    g.pictureBoard()


# if impossible, next piece is picked
def test_10(g):
    g.move()

    for i in range(7):
        assert isinstance(g.currentPiece, int)
        g.currentPiece += 1
        g.moveUntilUnthreatened()

    gameOver = g.checkGameOver()
    assert gameOver == False
    g.pictureBoard()


# if solution cannot be found, piece 1 is moved to next pos.
# a proof should be found along the column.
def test_11(g):
    nr = 1
    g.move()

    for i in range(nr,8):
        if g.currentPiece % 8 == 0:
            g.currentPiece = nr
        g.currentPiece += 1
        g.moveUntilUnthreatened()

    gameOver = g.checkGameOver()
    if not gameOver:
        g.currentPiece = nr
        g.move()
    assert g.standing[g.currentPiece-1] == [3,1]
    assert gameOver == False
    g.pictureBoard()


#
def test_12(g):
    nr = 1
    g.move()
    for n in range(7):
        for i in range(nr,8):
            if g.currentPiece % 8 == 0:
                g.currentPiece = nr
            g.currentPiece += 1
            g.moveUntilUnthreatened()

        gameOver = g.checkGameOver()
        if not gameOver:
            g.pictureBoard()
            g.currentPiece = nr
            g.move()
        else:
            break

    assert g.standing[g.currentPiece-1] == [1,1]
    assert gameOver == False
    g.pictureBoard()


# choose a nr to test a starting piece
def test_13(g):
    nr = 3
    g.currentPiece = nr
    g.move()
    for n in range(7):
        for i in range(8):
            if g.currentPiece % 8 == 0:
                g.currentPiece = 0
            g.currentPiece += 1
            if g.currentPiece != nr:
                g.moveUntilUnthreatened()

        gameOver = g.checkGameOver()
        if not gameOver:
            g.pictureBoard()
            g.currentPiece = nr
            g.move()
        else:
            break

    if gameOver:
        print("GAME OVER!")

    assert gameOver
    g.resetBoard()
    for i in range(len(g.standing)):
        assert g.standing[i][0] == 1
    g.pictureBoard()


#
def test_14(g):
    nr = 1
    for k in range(8):
        g.currentPiece = nr
        g.move()
        for n in range(7):
            for i in range(8):
                if g.currentPiece % 8 == 0:
                    g.currentPiece = 0
                g.currentPiece += 1
                if g.currentPiece != nr:
                    g.moveUntilUnthreatened()

            gameOver = g.checkGameOver()
            if not gameOver:
                g.pictureBoard()
                g.currentPiece = nr
                g.move()
            else:
                break

        if gameOver:
            g.pictureBoard()
            print("GAME OVER in", g.nrOfMoves, "moves")
            break

        g.resetBoard()
        for i in range(len(g.standing)):
            assert g.standing[i][0] == 1
        g.pictureBoard()

        nr += 1


# testing the game over function
def test_gameover(g):
    g.standing = [[2, 1], [5, 2], [7, 3], [1, 4], [3, 5], [8, 6], [6, 7], [4, 8]]
    gameOver = g.checkGameOver()
    assert gameOver


def test_r(g):
    g.standing = [[2, 1], [5, 2], [7, 3], [1, 4], [3, 5], [8, 6], [6, 7], [4, 8]]
    for i in g.standing:
        g.currentPiece = i[1]
        assert g.checkRow() == False

def test_d1(g):
    g.standing = [[2, 1], [5, 2], [7, 3], [1, 4], [3, 5], [8, 6], [6, 7], [4, 8]]
    for i in g.standing:
        g.currentPiece = i[1]
        assert g.checkUpRight() == False

def test_d2(g):
    g.standing = [[2, 1], [5, 2], [7, 3], [1, 4], [3, 5], [8, 6], [6, 7], [4, 8]]
    for i in g.standing:
        g.currentPiece = i[1]
        assert g.checkUpLeft() == False

def test_d3(g):
    g.standing = [[2, 1], [5, 2], [7, 3], [1, 4], [3, 5], [8, 6], [6, 7], [4, 8]]
    for i in g.standing:
        g.currentPiece = i[1]
        assert g.checkDownRight() == False

def test_d4(g):
    g.standing = [[2, 1], [5, 2], [7, 3], [1, 4], [3, 5], [8, 6], [6, 7], [4, 8]]
    for i in g.standing:
        g.currentPiece = i[1]
        assert g.checkDownLeft() == False
