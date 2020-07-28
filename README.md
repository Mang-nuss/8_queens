# 8_queens

The 8 queens are to be positioned so that no one of them threatens the position of another. A solution can be found using a step-by-step method.

Briefly,
1. Starting off with piece no 1, a piece is moved until it is not threatened (if possible).
2. Given this setting, the next pieces are moved alike.
3. The 7 pieces are considered in turn. When unthreatened, the piece is put into a List.
4. Assume there are at least 2 items in the List: x and y. A round is closed if x is to be tested again, without another piece y having been able to move since x was last tested.
5. A minimum request is that 7 pieces are moved along the column, since 2 pieces may not share row.
6. Thus, if (at least) 7 pieces have been moved and the 8th piece is not threatened, the goal is reached.

Some boolean attributes are used:
* isThreatened
* UnsuccessfullyTested (if every piece that isThreatened is also unsuccessfully tested, the piece last moved must be checked again. 
The track is checked back until the starting piece.)
* cannotBeMovedFirst (e.g., according to this method, the 2nd piece cannot be moved first)
* hasTriedEveryRow (e.g., the pieces 4 & 5 can initially be moved to the rows 6,7,8)
