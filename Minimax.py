import chess
import chess.svg
import time

moves = 0

def chessint():
    if request.method == 'POST':
        if board_state.turn:
            uci = request.form['move_post']
            move = chess.Move.from_uci(uci)
            print (move)
            if move in board_state.legal_moves:
                move = f"{move}"
                board_state.push_uci(move) #uses UCI
        else:
            uci = minimax()
            move = chess.Move.from_uci(uci)
            if move in board_state.legal_moves:
                move = f"{move}"
                board_state.push_san(move) #uses SAN
    return render_template('index.html', chessboard=chess.svg.board(board=board_state))

def value(board):
    value=0
    pieceValue = {
        "r":5,"n":3,"b":3,"q":9,"k":999,"p":1, \
        "R":-5,"N":-3,"B":-3,"Q":-9,"K":-999,"P":-1
    }
    fen = list(board.board_fen())
    for i in range (len(fen)):
        try:
            value = value + pieceValue[f"{fen[i]}"] #sum up the values
        except:
            pass
    return value

def legalmoves(board):
    return repr(board.legal_moves).split("(")[1][:-2] #legalmoves as string

def best_move(board ,depth, alpha, beta, maxplayer):
    global moves
    legal = legalmoves(board).split(", ")
    if depth == 0 or legal[0] == '':
        return value(board)
    if maxplayer:
        value0 = -9999
        childlist0 = []
        for c, x in enumerate(legal):
            board.push_san(x) #Does a move
            eval_max = minimax(board,depth-1,alpha, beta,False)
            childlist0.append(eval_max)
            maxindex0 = childlist0.index(max(childlist0))
            bestmove0 = legal[maxindex0]
            alpha = max(alpha, eval_max)
            board.pop()
            if alpha >= beta:
                break #Beta cut-off
            moves = moves+1
        return(bestmove0)

def minimax(board ,depth, alpha, beta, maxplayer):
    global moves
    legal = legalmoves(board).split(", ")
    if depth == 0 or board.is_game_over():
        return value(board)
    if maxplayer:
        childlist0 = []
        for c, x in enumerate(legal):
            board.push_san(x) #Does a move
            eval_max = minimax(board,depth-1,alpha, beta,False)
            alpha = max(alpha, eval_max)
            board.pop()
            if alpha >= beta:
                break #Beta cut-off
            moves = moves+1
        return alpha
   
    else:
        childlist1 = []
        for c, x in enumerate(legal):
            board.push_san(x) #Does a move
            eval_min = minimax(board,depth-1, alpha, beta,True)
            beta = min(beta, eval_min)
            board.pop()
            if alpha >= beta:
                break #Alpha cut-off
            moves = moves+1
        return beta

def run(board_state, depth):
    global moves
    moves = 0
    for i in range(1,depth+1):
        print("Depth:",i)
        start = time.time()
        recommended_move = best_move(board_state,i,-999,999,True)
        print("Minimax output:",recommended_move)
        end = time.time()
        print("Moves:",moves)
        print("Seconds:",end-start,)
        print("--------------------------------")
    return recommended_move

if __name__ == "__main__":
    state = chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")
    run(state, 2)
