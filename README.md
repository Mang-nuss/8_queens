# 8_queens

The 8 queens are to be positioned so that no one of them threatens the position of another. A solution can be found using a step-by-step method.

Briefly, x is set to 1 (that is, the first piece).
1. piece x takes one step along its column.
2. thereafter, the other pieces (8 except x) moves until they find empty spots, looping through them all.
3. if none of the pieces is able to move, x is set to 2.
4. all goes along until all pieces have found unthreatened spots.
