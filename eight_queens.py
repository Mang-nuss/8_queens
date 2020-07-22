#author: MJ
#2019-12-10

from piece import Piece

class Game:
    'the game object'

    def __init__(self,dimension):
        self.gameOver = False
        self.dimension = dimension
        self.positions = self.generateBoard(dimension)
        self.occupiedPositions = self.positions[:dimension]
        self.openPositions = self.positions[dimension:]
        
        self.setOfPieces = []
        self.firstMoves = []
        self.piecesThatCannotBeMovedFirst = []
        self.positionsOfTheTrial = []
        self.pieceNr = 1
        self.nrOfTrialsStarted = 0

        for i in range(dimension):
            piece = Piece(self.pieceNr)
            self.setOfPieces.insert(i, piece)
            piece.setCurrentPosition(self.positions[i])
            #piece.registerThreatenedPositions(dimension,piece.currentPosition)

            self.pieceNr += 1
        
        self.currentPiece = self.setOfPieces[0]

    """
    def updatePositions(self,pos): 
        self.openPositions.remove(pos)
        self.occupiedPositions.append(pos)
    def setCurrentPiece(self,piece): self.currentPiece = piece
    def getCurrentPiece(self): return self.currentPiece
    def generatePieceOutOfGivenPosition(self,pos):
    """

    #Get & Set methods
    def getCurrentPiece(self):
        #print("piece is:", game.currentPiece.getPieceId())
        return game.currentPiece
    
    def setCurrentPiece(self,pieceNr):
        game.currentPiece = game.setOfPieces[pieceNr-1]
        #print("Switching piece. Current piece is:", pieceNr)

    def getNrOfTrials(self):
        return game.nrOfTrialsStarted
    
    def setNrOfTrials(self,n):
        game.nrOfTrialsStarted = n
    
    def getFirstMoves(self):
        return game.firstMoves
    
    def setFirstMoves(self,pos):
        game.firstMoves.append(pos)

    def positionIsThreatened(self,pos):
        isThreatened = False
        for p in game.getCurrentPiece().getThreatensPositions():
            if p == pos:
                isThreatened = True
        return isThreatened

    def positionsAreReset(self):
        for i in range(dimension):
            piece = game.setOfPieces[i]
            piece.setCurrentPosition(self.positions[i])

    def theThreateningPieces(self,pos):
        arrayOfPieces = []
        if game.positionIsThreatened(pos):
            for p in game.setOfPieces:
                for t in p.threatensPositions:
                    if t == pos:
                        arrayOfPieces.append(p)
        return arrayOfPieces

    def addToPiecesThatCannotBeMovedFirst(self,pieceId):
        self.piecesThatCannotBeMovedFirst.append(pieceId)

    'the board'
    #Method: for each of the nr of rows, the row nr is put on index 0.
    #Thereafter, for each of the nr of columns (identical), the column nr is put on index 1 of the arrays.
    def generateBoard(self,dimension):
        positions = []
        nrOfPositions = dimension**2
        first = 0 #Since 0%8 == 0, below
        second = 0

        for i in range(nrOfPositions): #for every position on the board,
            if i % dimension == 0:
                first += 1; #after <dimension> positions, add 1 to the number that is put into the array.
                #positions[i][0] = first  #For each of the rows
            positions.append([first,0])
        
        for i in range(nrOfPositions): #for every position on the board,
            if i % dimension == 0:
                second = 1; #after <dimension> positions, add 1 to the number that is put into the array.
                #positions[i][0] = first  #For each of the rows
            positions[i][1] = second
            second += 1
        
        return positions
    
    'TDD session methods'
    def pictureBoard(self):
        print("\n")
        print("-------------------------------------------------")

        for rowNr in range(game.dimension):
            row = "|"
            for n in range(len(game.setOfPieces)):
                game.setCurrentPiece(n)
                piece = game.getCurrentPiece()
                pos = piece.getCurrentPosition()
                x = pos[0]
                y = pos[1]
                if x == rowNr+1:
                    row += "  X  |"
                else:
                    row += "     |"
            print(row)
            if rowNr != game.dimension-1:
                print("+-----+-----+-----+-----+-----+-----+-----+-----+")
            else:
                print("-------------------------------------------------")

    def move(self,piece):
        piece.threatensPositions.clear()
        currentPosition = piece.getCurrentPosition()
        newPos = [currentPosition[0]+1, currentPosition[1]]
        piece.setCurrentPosition(newPos)
        print("Move: Piece with id", piece.getPieceId(), "is now at", newPos)

    def pieceIsNow(self,id):
        game.setCurrentPiece(id)
        piece = game.getCurrentPiece()
        return piece

    # piece takes all positions in its column
    def pieceTakesNextPositionsInItsColumn(self,piece):
        p = self.pieceIsNow(piece)
        i = p.getCurrentPosition()[0]
        while i < self.dimension:
            self.move(p)
            i += 1

    def isThreatening(self,piece):

        print("----THREATEN CHECK----")
        threatened = False
        for p in range(len(game.setOfPieces)):
            game.setCurrentPiece(p+1)
            currentPiece = game.getCurrentPiece()
            if currentPiece.getCurrentPosition() in piece.threatensPositions:
                threatened = True
                break
                print("piece with id:", piece.getPieceId(),
                      "is threatening piece nr", currentPiece.getPieceId(),
                      "at position", currentPiece.getCurrentPosition())

        return threatened

    #TDD todo 1
    def pieceHasThreatenedPositions(self,piece,dimension):
        i=1
        while i != piece.getPieceId():
            game.setCurrentPiece(i)
            otherPiece = game.getCurrentPiece()
            print("current piece:", otherPiece.getPieceId())
            otherPiece.registerThreatenedPositions(dimension)
            if piece.getCurrentPosition() in otherPiece.getThreatensPositions():
                return True
            else:
                return False

    #TDD todo 2
    def pickNextPiece(self):
        piece = game.getCurrentPiece()
        #print('current pos: ', str(piece.getCurrentPosition()))
        nr = 0
        if piece.pieceId == game.dimension:
            nr = 1
        else:
            nr = piece.pieceId+1 
        game.setCurrentPiece(nr) #since length = dimension-1
        return game.getCurrentPiece()
        print("Pos of", piece.pieceId, "after switching to next piece: ", piece.getCurrentPosition())

    #Method to represent Trial Results
    def presentTrialResult(self):
        print("-----------------------")
        print("Registered items:")
        for p in game.getFirstMoves():
            print(p)
        print("Trial positions: ", game.positionsOfTheTrial)
        print("-----------------------")
    
    #Redundant on my particular strategy:
    def pickPreviousPiece(self): 
        piece = game.getCurrentPiece()
        print('current pos: ', str(piece.getCurrentPosition()))
        nr = 0
        if piece.pieceId == 0:
            nr = 8
        else:
            nr = piece.pieceId-1
        game.setCurrentPiece(nr) #since length = dimension-1
        print('next pos: ', piece.getCurrentPosition())
        
    #TDD todo 3

    
    #Helper method: is the move valid with regard to the first moves condition?
    def moveIsValid(self,pos): 
        print("moveIsValid?")      
        accepted = True
        p = game.getCurrentPiece()
        if len(game.getFirstMoves()) == 0:
            print("move to", pos, "is registered.")
            game.setFirstMoves(pos)
            accepted = True
            #Else, each of the previous ones are checked.
        if game.nrOfTrialsStarted > len(game.getFirstMoves()):
            print("in MoveIsValid if statement")
            for alreadyMade in game.getFirstMoves():
                print("checks", alreadyMade)
                if pos == alreadyMade:
                    print("move to", pos, "is not permitted.")
                    game.setFirstMoves(pos)
                    accepted = False
        #if game.moveIsToBeRegisteredInFirstMovesArray(p) == True:
            #accepted = True
        if accepted:
            print("move to", pos, "is valid")
        return accepted
            
    
    #TDD todo 4
    #Since two equal pieces are equivalently threatened/threatening, "is threatened" is sufficient
    def currentPosIsThreatened(self,pos):
        piece = game.getCurrentPiece()
        #print("current pos for piece", piece.pieceId, "is: ", cp)
        theOtherPieces = game.setOfPieces[:]
        theOtherPieces.pop(piece.pieceId-1) #excludes the piece itself from the iteration
        brr = []
        #print("in currentPieceIsThreatened")
        for p in theOtherPieces:
            brr.append(p.getCurrentPosition())
        #print("the other pieces' positions: ", brr)
        threatened = False
        for p in theOtherPieces:
            #print("id: ", p.pieceId)
            for position in p.getThreatensPositions():
                #print("pos:", position)
                if pos == position:
                    threatened = True
                    break
        
        return threatened
    
    ##TDD todo 5    

    def makeMoves(self):
        piece = game.getCurrentPiece()
        pos = piece.getCurrentPosition()
        nrOfMoves = 0
        #print("stops when unthreatened..?")
        while nrOfMoves <= game.dimension:
            str = "piece", piece.getPieceId(), "considered pos:", pos
            print(str)
            if game.currentPosIsThreatened(pos) == False:
                if game.moveIsValid(pos) == True:
                    piece.setCurrentPosition(pos)
                    piece.clearThreatensPositions()
                    piece.registerThreatenedPositions(pos) #right?
                    piece.cannotBeMoved == False
                    break
            #If threatened
            else:
                piece.setCurrentPosition(pos)
                piece.clearThreatensPositions()
                piece.registerThreatenedPositions(pos) #right?
                piece.cannotBeMoved == False
                piece.cannotBeMoved == True

            pos = game.takeNext(pos)
            nrOfMoves+=1
        
        if piece.cannotBeMoved:
            game.pieceStaysAt(piece.getCurrentPosition())

    #Helper method
    def takeNext(self,pos):
        rowNumber = pos[0]
        colNumber = pos[1]
        if rowNumber == game.dimension:
            rowNumber = 1
        else:
            rowNumber = rowNumber+1
        pos = [rowNumber,colNumber]
        return pos

    #Helper method
    def pieceStaysAt(self,pos):
        print("stays")
        p = game.getCurrentPiece()
        p.setCurrentPosition(pos)
        p.clearThreatensPositions()
        p.registerThreatenedPositions(pos)
    
    #Helper method: returns True if move hasn't been tried yet
    def moveIsToBeRegisteredInFirstMovesArray(self, piece):
        moveNotYetTried = True
        #the nr of trials should equal the nr of first moves
        if game.nrOfTrialsStarted >= len(game.getFirstMoves()):
            if len(game.firstMoves) != 0:
                for pos in game.getFirstMoves():
                    #print("for loop started")
                    if piece.getCurrentPosition() == pos:
                        print(pos, "is already tried!!!")
                        moveNotYetTried = False
            #move is registered IF it has not before been tried as first move
            if moveNotYetTried == True:
                print("move to", piece.getCurrentPosition(), "is registered.")
                game.setFirstMoves(piece.getCurrentPosition())

        return moveNotYetTried

    #Helper method
    def firstMoveIsRegistered(self):
        pos = game.getCurrentPiece().getCurrentPosition()
        game.setFirstMoves(pos)

    #TDD todo 6
    def pickNewPiece(self):
        #game.pickNextPiece()
        p = game.getCurrentPiece()
        print("picked piece: ", p.pieceId, "at", p.getCurrentPosition())
        if game.currentPosIsThreatened(p.getCurrentPosition()) == False:
            #print("Switches to next ---")
            game.pickNextPiece()

        #game.makeMoves()
    
    #TDD todo 8
    def newSetup(self):
        game.addToNrOfTrials() #One (more) trial is started.
        n = 0
        print("new setup:")
        for piece in game.setOfPieces:
            piece.setCurrentPosition(game.positions[n])
            #print(game.positions[n])
            piece.clearThreatensPositions()
            piece.registerThreatenedPositions(piece.currentPosition)
            n += 1
        game.setCurrentPiece(1) #starts over fron piece no 1
    
    #Helper method
    def addToNrOfTrials(self):
        nr = game.nrOfTrialsStarted + 1
        game.setNrOfTrials(nr)
    
    #TDD todo 9
    def tryAllPieces(self):
        print("tryAllPieces is initiated")
        game.makeMoves()
        for i in range(game.dimension): #since it has to be iterated 7 times to reach back
            game.pickNewPiece()
        #print("piece is: ", game.getCurrentPiece().pieceId)
    
    #TDD todo 10
    def checkIfSolutionIsReached(self):
        print("CHECKAR!")
        game.gameOver = True
        for p in game.setOfPieces:
            game.setCurrentPiece(p.pieceId)
            if game.currentPosIsThreatened(p.getCurrentPosition()): 
                print("threatened")
                game.gameOver = False
                break
            #print("not threatened..?")
    
    #TDD todo 12
    def keepOnSearchingForUnthreatenedPos(self):
        #p = g.getCurrentPiece()
        pass

    #TDD todo
    def trialIsOver(self):
        over = False
        for p in game.setOfPieces:
            if p.hasBeenConsideredAtLeastOnce == False:
                over = False
                break
            else:
                over = True
        return over
            

    #TDD todo 13
    def fullGame(self):
        print("fullgame")
        for i in range(3):
            print("i=", i)
            game.newSetup()
            print("started trials: ", game.nrOfTrialsStarted)
            arr = []
            for p in game.setOfPieces:
                arr.append(p.getCurrentPosition())
            print("Positions are: ", arr)
            game.tryAllPieces()
            
            game.checkIfSolutionIsReached()
            #game.newSetup()
            print("first moves (length): ", len(game.getFirstMoves()), "i.e.", game.getFirstMoves())
            if game.gameOver:
                solution = []
                first = game.getFirstMoves()[-1]
                for p in game.setOfPieces:
                    solution.append(p.getCurrentPosition())
                print("Solution found. Positions are: ", solution, "with first move: ", first)
                break
        print("DONE!")
    
    def testing(self):
        pos = game.getCurrentPiece().getCurrentPosition()
        for i in range(2):
            print()
            print("NEW TRIAL")
            print()
            for i in range(game.dimension):            
                game.makeMoves()
                game.pickNextPiece()


##-------------------------------------------------------------------------------##

"""
for piece in game.setOfPieces:
    piece.registerThreatenedPositions(piece.currentPosition)
    print(str(piece.currentPosition))
"""
print("startar!")
solutionFound = False
dimension = 8
numberOfMoves = 0
game = Game(dimension)

def main():     
    """
    #game.currentPieceIsThreatened()
    for piece in game.setOfPieces:
        print("piece ", piece.pieceId, " is on ", piece.currentPosition)
    game.pickNewPiece()
    
    pos = [1,1]
    for piece in game.theThreateningPieces(pos):
        print("id:", piece.getPieceId())
    game.setCurrentPiece(1)
    p = game.getCurrentPiece()
    #print(p.getCurrentPosition(), ",", p.getThreatensPositions())
    for i in range(8):
        game.makeMoves()
    print(p.getCurrentPosition(), ",", p.getThreatensPositions())
    """
    game.testing()
    """
    Condition C: is it possible to find a unique spot (row & column) for each piece, where the diagonals do not connect?
    This strategy starts off by placing every piece on row no 1. The first solution will be found by moving piece no 4 to
    pos E4. 

    1. 1st piece (A1) will not find an open place (due to the chess rules R). Instead, start with the 2nd one (A2).
    2. Stop when finding an open place (will be H2).
    3. Next piece (A3).
        - for all the original-positioned pieces: if there is no open place, take next one.
        - start over. A1 will find an open place, since there is one piece (A2) that was moved away from its
            threatening position. I.e., A1 will find a place at B1.
    4. Question: will this pattern "reinforce"? Otherwise, C cannot be met.
    5. What if all pieces have been looped through? 
    """


    #print("hello")
    """
    while solutionFound == False:
        if numberOfMoves > 20:
            quit
        else:
            move(board)

    print("ended. Winner is: ", player)
    """

##-------------------------------------------------------------------------------##



#game = Game(8)
#piece = Piece(game.pieceNr)

def testRegisterThreatenedPositions(thePiece,pos):
    thePiece.registerThreatenedPositions(thePiece,pos)
    result = thePiece.threatensPositions
    print(result)
    return

position = [1,1]
#testRegisterThreatenedPositions(board,piece,position)
dimension = 8
print(dimension**2)

if __name__ == "__main__":
    main()


"""
#Method: for each of the nr of rows, the row nr is put on index 0.
    #Thereafter, for each of the nr of columns (identical), the column nr is put on index 1 of the arrays.
def generateBoard(dimension):
        positions = []
        nrOfPositions = dimension**2
        first = 0 #Since 0%8 == 0, below
        second = 0

        for i in range(nrOfPositions): #for every position on the board,
            if i % dimension == 0:
                first += 1; #after <dimension> positions, add 1 to the number that is put into the array.
            #positions[i][0] = first  #For each of the rows
            positions.append([first,0])
        
        for i in range(nrOfPositions): #for every position on the board,
            if i % dimension == 0:
                second = 1; #after <dimension> positions, add 1 to the number that is put into the array.
            #positions[i][0] = first  #For each of the rows
            positions[i][1] = second
            second += 1
        
        return positions
"""
def testGenerateBoard(d,game):
    result = game.generateBoard(d)
    #print(result)
    #print(len(result))
    return result
"""
result = game.generateBoard(dimension)
#print(result)
occs = result[:7]
#print('occs: ',occs)
ops = result[7:]
#print('ops: ',ops)
"""
def testPrintOutPieceData(game):
    for i in game.setOfPieces:
        print("size:", len(i.threatensPositions))
        for p in i.threatensPositions:
            print("testar", p)

def testPositionIsThreatened(game,position):

    for piece in game.setOfPieces:
        print("id:", piece.pieceId)
        for pos in piece.threatensPositions:
            if pos == position:
                return True
            else:
                return False



