import tkinter as tk
from PIL import Image,ImageTk
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
                if min(currRow, currCol) < 0 or max(currRow, currCol) > 7:
                    break

                other = board[currRow][currCol]
                if other is None or (self.__repr__().islower() != other.__repr__().islower()):
                    result.append(Position(currRow , currCol))
                
                if other is not None:
                    break
        return result
    
    def __repr__(self) -> str:
        return self.repr

class ChessBoard(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)

        self.pieceSteps = {"p": 1, "r": 8, "b": 8, "n": 1, "q": 8, "k": 1}
        self.pieceDirection = {
            "p": [Direction(1, 0)],
            "r": [Direction(1, 0), Direction(-1, 0), Direction(0, 1), Direction(0, -1)],
            "b": [Direction(1, 1), Direction(-1, 1), Direction(1, -1), Direction(-1, -1)],
            "n": [Direction(2, 1), Direction(-2, 1), Direction(2, -1), Direction(-2, -1),
                  Direction(1, 2), Direction(-1, 2), Direction(1, -2), Direction(-1, -2)],
        }
        self.pieceDirection["q"] = self.pieceDirection["r"] + self.pieceDirection["b"] 
        self.pieceDirection["k"] = self.pieceDirection["q"]

        self.cellSize = 75
        self.board = self.initBoard()
        self.positions = self.getPositions()
        self.pieces = self.init_pieces()
        self.selectedCell = None
        self.move_suggestions = []
        
        self.geometry("1000x1500")
        self.canvas = tk.Canvas(self, width=1000, height=1500)
        self.canvas.pack()
        self.canvas.bind("<1>", self.clickHandler)
        self.update()
        self.mainloop()

    def initBoard(self):
        fen = "rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR"
        board = [[None] * 8 for _ in range(8)]
        for row, row_fen in enumerate(fen.split("/")):
            col = 0
            for ch in row_fen:
                if (ch.isdigit()):
                    col += int(ch)
                else:
                    board[row][col] = ChessPiece(ch, self.pieceDirection[ch.lower()], self.pieceSteps[ch.lower()])
                    col += 1
        return board 
    
    def init_pieces(self):
        return {repr: ImageTk.PhotoImage(Image.open("./imgs/"+repr+".png")) for repr in self.positions}
    
    def draw_grid(self):
        windowSize = self.cellSize * 8
        for i in range(1, 10):
            self.canvas.create_line(self.cellSize, i * self.cellSize, self.cellSize + windowSize, i * self.cellSize)
            self.canvas.create_line(i * self.cellSize, self.cellSize, i * self.cellSize, self.cellSize + windowSize)

    def draw_suggestions(self):
        for suggestion in self.move_suggestions:
            col = (suggestion.col + 1) * self.cellSize
            row = (suggestion.row + 1) * self.cellSize
            self.canvas.create_rectangle(col, row, col + self.cellSize, row + self.cellSize, outline="#fb0", fill="#fb0")

    def getPositions(self):
        out = {}
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell != None:
                    rpr = cell.__repr__() if cell.__repr__().islower() else "w"+cell.__repr__().lower()
                    pos = Position((i+1)*self.cellSize, (j+1)*self.cellSize)
                    if rpr in out:
                        out[rpr].append(pos)
                    else:
                        out[rpr] = [pos]
        return out

    def clickHandler(self, event):
        col = (event.x // self.cellSize) - 1
        row = (event.y // self.cellSize) - 1
        if max(row, col) < 8 and min(row,col)  >= 0:
            clickPosition = Position(row, col)
            if self.selectedCell is None:
                self.selectedCell = clickPosition
                self.move_suggestions = self.getMoves(clickPosition)
            else:
                self.movePeice(self.selectedCell, clickPosition)
                self.positions = self.getPositions()
                self.selectedCell = None
                self.move_suggestions = []
        self.update()
        
    def movePeice(self, origin: Position, destination: Position):        
        self.board[destination.row][destination.col] = self.board[origin.row][origin.col]
        self.board[origin.row][origin.col] = None

    def getMoves(self, position: Position) -> list:
        return self.board[position.row][position.col].getMoves(self.board, position)
    
    def update(self) -> None:
        super().update()
        self.canvas.delete(tk.ALL)
        self.draw_grid()
        self.draw_suggestions()
        for repr in self.positions:
            for pos in self.positions[repr]:
                self.canvas.create_image(pos.col + 8,pos.row + 8,anchor=tk.NW,image=self.pieces[repr] ) 

if __name__ == "__main__":
    board = ChessBoard()