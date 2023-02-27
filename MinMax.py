
import copy

def get_best_move(board: list, isBlackTurn: bool, getAllMoves, movePeice, depth = 3) -> list:
    return max(board, isBlackTurn, getAllMoves, movePeice, depth)[1]

def max(board: list, isBlackTurn: bool, getAllMoves, movePeice, depth: int) -> int:
    if depth == 0:
        return score(board, isBlackTurn), None
    
    maxScore = -float("inf")
    bestMove = None
    for move in getAllMoves(board, isBlackTurn):

 
        prev = board[move.destination.row][move.destination.col]
        board[move.destination.row][move.destination.col] = board[move.origin.row][move.origin.col]
        board[move.origin.row][move.origin.col] = None

        moveScore, _ = min(board, not isBlackTurn, getAllMoves, movePeice, depth-1)
        if moveScore > maxScore:
            maxScore = moveScore
            bestMove = move
        
        board[move.origin.row][move.origin.col] = board[move.destination.row][move.destination.col]
        board[move.destination.row][move.destination.col] = prev


    return maxScore, bestMove

def min(board: list, isBlackTurn: bool, getAllMoves, movePeice, depth: int) -> int:
    if depth == 0:
        return score(board, isBlackTurn), None
    
    minScore = float("inf")
    bestMove = None
    for move in getAllMoves(board, isBlackTurn):
        
        prev = board[move.destination.row][move.destination.col]
        board[move.destination.row][move.destination.col] = board[move.origin.row][move.origin.col]
        board[move.origin.row][move.origin.col] = None

        moveScore, _ = max(board, not isBlackTurn, getAllMoves, movePeice, depth-1)
        if moveScore < minScore:
            minScore = moveScore          
            bestMove = move
        
        board[move.origin.row][move.origin.col] = board[move.destination.row][move.destination.col]
        board[move.destination.row][move.destination.col] = prev

    return minScore, bestMove

scores = {
    "p":1,
    "b":3,
    "n":3,
    "r":5,
    "q":15,
    "k":1e+6,
}

def score(board: list, isBlackTurn: bool) -> int:
    blakcScore, whiteScore = 0,0
    for row in board:
        for cell in row:
            if cell is None:
                continue
            piece = cell.__repr__()
            if piece.islower():
                blakcScore+= scores[piece]
            else:
                whiteScore += scores[piece.lower()] 
    return blakcScore - whiteScore if not isBlackTurn else whiteScore - blakcScore    

