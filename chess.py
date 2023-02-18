from collections import namedtuple

Position = namedtuple("Position", "row col")
Direction = namedtuple("Direction", "rowOffset colOffset")

class ChessPiece:
    def __init__(self, repr: str, move_directions: list, nSteps: int) -> None:
        self.repr = repr
        self.nSteps = nSteps
        self.move_directions = move_directions

    def getMoves(self, board: list, currPosition: Position):
        result = []
        for dir in self.move_directions:
            for step in range(1, self.nSteps+1):
                currRow = currPosition.row + dir.rowOffset * step
                currCol = currPosition.col + dir.colOffset * step
                if min(currRow, currCol) >= 0 and max(currRow, currCol) < 8:
                    result.append(Position(currRow , currCol))
        return result
    
    def __repr__(self) -> str:
        return self.repr

class ChessBoard:
    def __init__(self) -> None:
        
        self.pieceDirection = {
            "p": [Direction(1, 0)],
            "r": [Direction(1, 0), Direction(-1, 0), Direction(0, 1), Direction(0, -1)],
            "b": [Direction(1, 1), Direction(-1, 1), Direction(1, -1), Direction(-1, -1)],
            "n": [Direction(2, 1), Direction(-2, 1), Direction(2, -1), Direction(-2, -1),
                  Direction(1, 2), Direction(-1, 2), Direction(1, -2), Direction(-1, -2)],
        }
        self.pieceDirection["q"] = self.pieceDirection["r"] + self.pieceDirection["b"] 
        self.pieceDirection["k"] = self.pieceDirection["q"]

        self.nSteps = {"p": 1, "r": 8, "b": 8, "n": 1, "q": 8, "k": 1}
        self.board = self.initBoard()

    def initBoard(self):
        fen = "rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR"
        board = [[None] * 8 for _ in range(8)]
        for row, row_fen in enumerate(fen.split("/")):
            col = 0
            for ch in row_fen:
                if (ch.isdigit()):
                    col += int(ch)
                else:
                    board[row][col] = ChessPiece(ch, self.pieceDirection[ch.lower()], self.nSteps[ch.lower()])
                    col += 1
        return board 
    
    def getMoves(self, position: Position) -> list:
        return self.board[position.row][position.col].getMoves(board, position)

    def display(self) -> None:
        [print(row) for row in self.board]

board = ChessBoard()
board.display()
print(board.getMoves(Position(0, 1)))