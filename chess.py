import tkinter as tk
from PIL import Image,ImageTk
from collections import namedtuple
import random
from MinMax import get_best_move

Position = namedtuple("Position", "row col")
Direction = namedtuple("Direction", "rowOffset colOffset")
Move = namedtuple("Move", "origin destination")
class ChessPiece:
    def __init__(self, symbol: str, move_directions: list, nSteps: int) -> None:
        self.symbol = symbol
        self.nSteps = nSteps
        self.move_directions = move_directions
        
        self.getMoves = self.getPawnMoves if symbol.lower() == "p" else self.getMoves_

    def isOpponent(self, other):
        return self.__repr__().islower() != other.__repr__().islower()
    
    def getMoves_(self, board: list, currPosition: Position):
        result = []
        for direction in self.move_directions:
            for step in range(1, self.nSteps+1):
                currRow = currPosition.row + direction.rowOffset * step
                currCol = currPosition.col + direction.colOffset * step
                if min(currRow, currCol) < 0 or max(currRow, currCol) > 7:
                    break

                other = board[currRow][currCol]
                if other is None or self.isOpponent(other):
                    result.append(Position(currRow , currCol))
                
                if other is not None:
                    break
        return result
    
    def getPawnMoves(self, board: list, currPosition: Position):
        result = []
        rowOffset = 1 if self.symbol.islower() else -1
        forward = Position(currPosition.row + rowOffset, currPosition.col)
        
        if board[forward.row][forward.col] == None:
            result.append(forward)
        if (currPosition.row == 1 and self.symbol.islower()) or (currPosition.row == 6 and not self.symbol.islower()):
            towStepsForward = Position(currPosition.row + (2*rowOffset), currPosition.col)
            if board[towStepsForward.row][towStepsForward.col] == None:
                result.append(towStepsForward)
        
        forwardLeft = Position(currPosition.row + rowOffset, currPosition.col + 1)
        if currPosition.col < 7 and board[forwardLeft.row][forwardLeft.col] != None and self.isOpponent(board[forwardLeft.row][forwardLeft.col]):
            result.append(forwardLeft)
        forwardRight = Position(currPosition.row + rowOffset, currPosition.col - 1)
        if currPosition.col > 0 and board[forwardRight.row][forwardRight.col] != None and self.isOpponent(board[forwardRight.row][forwardRight.col]):
            result.append(forwardRight)
        
        return result

    
    def __repr__(self) -> str:
        return self.symbol

class ChessGame(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)

        self.chessBoard = ChessBoard()
        self.cellSize = 75

        self.selectedCell = None
        self.move_suggestions = []
        self.positions = self.getPositions()
        self.pieces = self.init_pieces()
        self.bestMove = self.chessBoard.getBestMove()

        self.geometry("1000x1500")
        self.canvas = tk.Canvas(self, width=1000, height=1500)
        self.canvas.pack()
        self.canvas.bind("<1>", self.clickHandler)
        self.update()
        self.mainloop()

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
        
        if self.bestMove is None:
            return
        
        for position in [self.bestMove.origin, self.bestMove.destination]:
            col = (position.col + 1) * self.cellSize
            row = (position.row + 1) * self.cellSize
            self.canvas.create_rectangle(col, row, col + self.cellSize, row + self.cellSize, fill="green")
    
    def init_pieces(self):
        return {repr: ImageTk.PhotoImage(Image.open("./imgs/"+repr+".png")) for repr in self.positions}
    
    def getPositions(self):
        out = {}
        for i, row in enumerate(self.chessBoard.board):
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
        if  0 <= row < 8 and 0 <= col < 8:
            clickPosition = Position(row, col)
            piece = self.chessBoard.board[clickPosition.row][clickPosition.col]
            if self.selectedCell is None and piece != None and (piece.__repr__().islower() == self.chessBoard.isBlackTurn):
                self.selectedCell = clickPosition
                self.move_suggestions = self.chessBoard.getMoves(clickPosition)
            else:
                if clickPosition in self.move_suggestions:
                    self.chessBoard.movePeice(Move(self.selectedCell, clickPosition))
                    self.positions = self.getPositions()
                    self.bestMove = self.chessBoard.getBestMove()
                self.selectedCell = None
                self.move_suggestions = []
        self.update()
    
    def update(self) -> None:
        super().update()
        self.canvas.delete(tk.ALL)
        self.draw_grid()
        self.draw_suggestions()
        for repr in self.positions:
            for pos in self.positions[repr]:
                self.canvas.create_image(pos.col + 8,pos.row + 8,anchor=tk.NW,image=self.pieces[repr] ) 

class ChessBoard():
    def __init__(self) -> None:

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

        self.isBlackTurn = True
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
                    board[row][col] = ChessPiece(ch, self.pieceDirection[ch.lower()], self.pieceSteps[ch.lower()])
                    col += 1
        return board 
        
    def movePeice(self, move: Move, board = None):        
        if board is None:
            board = self.board
        board[move.destination.row][move.destination.col] = board[move.origin.row][move.origin.col]
        board[move.origin.row][move.origin.col] = None
        self.isBlackTurn = not self.isBlackTurn

    def getlAllMoves(self, board, isBlackTurn: bool) -> list:
        allMoves = []
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell != None and (isBlackTurn == cell.__repr__().islower()):
                    origin = Position(i, j)
                    for destination in self.getMoves(origin, board):
                        allMoves.append(Move(origin, destination))
        random.shuffle(allMoves)
        return allMoves        
        
    def getMoves(self, position: Position, board = None) -> list:
        if board is None:
            board = self.board
        return board[position.row][position.col].getMoves(board, position)
    
    def getBestMove(self):
         return get_best_move(self.board, self.isBlackTurn, self.getlAllMoves, self.movePeice)   

if __name__ == "__main__":
    ChessGame()