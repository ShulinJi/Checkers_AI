# Checkers_AI
It will solve the puzzle assuming that both players are moving optimally.
Rules that it follows:

Starting Position: Each player starts with 12 pieces on the dark squares of the three rows closest to that player's side. The black pieces start from the top three rows, and the red ones start from the bottom three. The red player makes the first move.
Move Rules: There are two different ways to move.
Simple move (see the left image in the figure above): A simple move involves moving a piece one square diagonally to an adjacent unoccupied dark square. Normal pieces can move diagonally forward only; kings can move in any diagonal direction. (For the black player, forward is down. For the red player, forward is up.)
Jump (see the middle image in the figure above): A jump consists of moving a piece diagonally adjacent to an opponent's piece to an empty square immediately beyond it in the same direction (thus "jumping over" the opponent's piece front and back.) Normal pieces can jump diagonally forward only; kings can jump in any diagonal direction. A jumped piece is "captured" and removed from the game. Any piece, king or normal, can jump a king.
Jumping is mandatory. If a player has the option to jump, they must make it, even if doing so results in a disadvantage for the jumping player. 
Multiple jumps (see the right image in the figure above): After one jump, if the moved piece can jump another opponent's piece, it must keep jumping until no more jumps are possible, even if the jump is in a different diagonal direction. If more than one multi-jump is available, the player can choose which piece to jump with and which sequence of jumps to make. The sequence chosen is not required to be the one that maximizes the number of jumps in turn. However, a player must make all the available jumps in the sequence chosen.
Kings:
If a piece moves into the last row on the opponent's side of the board, it becomes a king and can move both forward and backward. A red piece becomes king when it reaches the top row, and a black piece becomes king when it reaches the bottom row. 
If a piece becomes a king, the current move terminates; The piece cannot jump back as in a multi-jump until the next move.
End of Game: A player wins by capturing all the opponent's pieces or when the opponent has no legal moves left.

Usage:  python3 checkers.py --inputfile <input file> --outputfile <output file>
