#author: MJ
#2019-12-11

class  Piece:

    def __init__(self,nr):
        self.pieceId = nr
        self.currentPosition = []
        self.threatensPositions = []
        self.cannotBeMoved = False
        self.hasBeenConsideredAtLeastOnce = False
        self.cannotBeMovedFirst = False

    def setCurrentPosition(self,position): self.currentPosition = position
    def getCurrentPosition(self):
        #print("position of piece is:", self.currentPosition)
        return self.currentPosition
    def clearThreatensPositions(self): self.threatensPositions[:] = []
    def addToThreatensPositions(self,position): self.threatensPositions.append(position)
    def getThreatensPositions(self): return self.threatensPositions
    def getPieceId(self):
        #print("piece id:", self.pieceId)
        return self.pieceId

    #Method: collecting the checking methods
    def registerThreatenedPositions(self,dimension):
        self.checkRow(dimension)
        self.checkUpLeft()
        self.checkDownLeft(dimension)
        self.checkUpRight(dimension)
        self.checkDownRight(dimension)
        #print("threatened for id", self.pieceId, "are", self.threatensPositions)

    #row-wise
    def checkRow(self,dimension):

        row = self.currentPosition[0]
        print("-----------------------\nchecking row:")
        for i in range(dimension): #Default: 8x8!

            if i+1 != self.currentPosition[1]:
                self.addToThreatensPositions([row,i+1])
                print([row,i+1])

    #up-left
    def checkUpLeft(self):

        row = self.getCurrentPosition()[0]
        col = self.getCurrentPosition()[1]
        print("checking up left for piece with starting pos", col, ":")
        while row > 1 and col > 1:
            row -= 1
            col -= 1
            self.addToThreatensPositions([row,col])
            print([row,col])
    
    #down-left
    def checkDownLeft(self,dimension):

        row = self.getCurrentPosition()[0]
        col = self.getCurrentPosition()[1]
        print("checking down left for piece with starting pos", col, ":")
        while row < dimension and col > 1:
            row += 1
            col -= 1
            self.addToThreatensPositions([row,col])
            print([row,col])

    #up-right
    def checkUpRight(self,dimension):

        row = self.getCurrentPosition()[0]
        col = self.getCurrentPosition()[1]
        print("checking up right for piece with starting pos", col, ":")
        while row > 1 and col < dimension:
            row -= 1
            col += 1
            self.addToThreatensPositions([row,col])
            print([row,col])

    #down-right
    def checkDownRight(self,dimension):

        row = self.getCurrentPosition()[0]
        col = self.getCurrentPosition()[1]
        print("checking down right for piece with starting pos", col, ":")
        while row < dimension and col < dimension:
            row += 1
            col += 1
            self.addToThreatensPositions([row,col])
            print([row,col])

                
    def positionIsThreatened(self,game,pos):

        threatened = False

        for i in range(len(game.positions)+1):
            if pos == game.positions[i]:
                threatened = True
        return threatened
    
            



