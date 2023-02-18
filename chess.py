class Direction:
    def __init__(self, rowOffset: int, colOffset: int) -> None:
        self.rowOffset = rowOffset
        self.colOffset = colOffset

class Position:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

class ChessPiece:
    def __init__(self, repr: str, move_directions: list, nSteps: int) -> None:
        self.repr = repr
        self.nSteps = nSteps
        self.move_directions = move_directions

    def getMoves(self, board: list[list], currPosition: Position):
        result = []
        for dir in self.move_directions:
            result.extend(self._getMoves(board, dir, currPosition))
        return result

    def _getMoves(self, board: list, dir: Direction, currPosition: Position):
        result = []
        for step in range(1, self.nSteps+1):
            currRow = currPosition.row + dir.rowOffset * step
            currCol = currPosition.col + dir.colOffset * step
            if min(currRow, currCol) >= 0 and max(currRow, currCol) < 8:
                result.append([currRow , currCol])
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

        self.nSteps = {
            "p": 1,
            "r": 8,
            "b": 8,
            "n": 1,
            "q": 8,
            "k": 1
        }
        self.board = self.initBoard()

    def initBoard(self):
        fen = "rbnkqnbr/pppppppp/8/8/8/8/PPPPPPPP/RBNKQNBR"
        board = [[None] * 8 for _ in range(8)]
        for i, row_fen in enumerate(fen.split("/")):
            col = 0
            for j, ch in enumerate(row_fen):
                if (ch.isdigit()):
                    col += int(ch)
                else:
                    board[i][col] = ChessPiece(ch, self.pieceDirection[ch.lower()], self.nSteps[ch.lower()])
                    col += 1
        return board 
    
    def getMoves(self, position: Position) -> list:
        return self.board[position.row][position.col].getMoves(board, position)

    def display(self) -> str:
        for row in self.board:
            print(row)
    

board = ChessBoard()
board.display()
print(board.getMoves(Position(0, 0)))