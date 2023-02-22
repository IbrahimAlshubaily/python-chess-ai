
import copy
def eval_moves(board: list, isBlackTurn: bool, getAllMoves, movePeice, depth = 3) -> list:
    result = {}
    bestMove = None
    bestScore =  - float("inf")
    for move in getAllMoves(board, isBlackTurn):
        boardCopy = copy.deepcopy(board)
        movePeice(boardCopy, move)
        result[move] = min(boardCopy, isBlackTurn, getAllMoves, movePeice, depth - 1)
        if result[move] > bestScore:
            bestScore = result[move]
            bestMove = move

    return bestMove


def max(board: list, isBlackTurn: bool, getAllMoves, movePeice, depth: int) -> int:
    if depth == 0:
        return score(board, isBlackTurn)
    
    maxScore = -float("inf")
    for move in getAllMoves(board, not isBlackTurn):
        boardCopy = copy.deepcopy(board)
        movePeice(boardCopy, move)
        moveScore = min(boardCopy, isBlackTurn, getAllMoves, movePeice, depth-1)
        if moveScore > maxScore:
            maxScore = moveScore
    return maxScore

def min(board: list, isBlackTurn: bool, getAllMoves, movePeice, depth: int) -> int:
    if depth == 0:
        return score(board, isBlackTurn)
    
    minScore = float("inf")
    for move in getAllMoves(board, isBlackTurn):
        boardCopy = copy.deepcopy(board)
        movePeice(boardCopy, move)
        moveScore = max(boardCopy, isBlackTurn, getAllMoves, movePeice, depth-1)
        if moveScore < minScore:
            minScore = moveScore
    return minScore

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
    return blakcScore - whiteScore if isBlackTurn else whiteScore - blakcScore    

