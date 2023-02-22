
import copy

def eval_moves(board: list, isBlackTurn: bool, getAllMoves, movePeice, depth = 3) -> list:
    #if isBlackTurn:
    return max(board, isBlackTurn, getAllMoves, movePeice, depth)[1]
    #return min(board, isBlackTurn, getAllMoves, movePeice, depth)[1]
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
        return score(board, isBlackTurn), None
    
    maxScore = -float("inf")
    bestMove = None
    for move in getAllMoves(board, isBlackTurn):
        boardCopy = copy.deepcopy(board)
        movePeice(boardCopy, move)
        moveScore, _ = min(boardCopy, not isBlackTurn, getAllMoves, movePeice, depth-1)
        if moveScore > maxScore:
            maxScore = moveScore
            bestMove = move
    return maxScore, bestMove

def min(board: list, isBlackTurn: bool, getAllMoves, movePeice, depth: int) -> int:
    if depth == 0:
        return score(board, isBlackTurn), None
    
    minScore = float("inf")
    bestMove = None
    for move in getAllMoves(board, isBlackTurn):
        boardCopy = copy.deepcopy(board)
        movePeice(boardCopy, move)
        moveScore, _ = max(boardCopy, not isBlackTurn, getAllMoves, movePeice, depth-1)
        if moveScore < minScore:
            minScore = moveScore          
            bestMove = move

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

