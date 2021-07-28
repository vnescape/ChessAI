# import Flask class
from flask import Flask, render_template, request, Markup
import chess
import chess.svg
import Minimax as ai
import re

def check_game_state():
    if board.outcome() is None:
        return 1
    elif board.outcome().result() == "1-0":
        return render_template('note.html', note="You've won!")
    elif board.outcome().result() == "0-1":
        return render_template('note.html', note="You've lost!")
    elif board.outcome().result() == "1/2-1/2":
        return render_template('note.html', note="Draw!")

# Input sanitization
def parse_input():
    if request.form["response"] == "Reset":
        # magic reset return
        return 132
    player_move_raw = request.form["response"]
    # restrict valid characters
    player_move = re.sub('[^a-h1-8|O\-O]', '', player_move_raw.lower())
    # restrict length of input
    if len(player_move) > 4:
        return render_template('note.html', note="Input too long.\
             Go back and chose one of these moves: " + ai.legalmoves(board))
    return player_move

def do_user_move(user_input):
    # check if the game is already over
    ret = check_game_state()
    legal = ai.legalmoves(board)
    # Save return value. Thus only one function call is necessary
    if ret != 1:
        return ret
    try:
        board.push_san(user_input)
        return 1
    except:
        return render_template('note.html', note="Illegal move. \
            Go back and chose one of these moves: " + legal)

def do_ai_move():
    # check if the game is already over
    ret = check_game_state()
        # Save return value. Thus only one function call is necessary
    if ret != 1:
        return ret
    ai_move = ai.run(board, depth)
    board.push_san(ai_move)
    return 1
    
depth = 4
board = chess.Board()

# create instance of Flask class
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    # I shouldn't be using globals...
    # It can cause confusion
    global board
    if request.method == "GET":
        return render_template('index.html', svg=Markup(chess.svg.board(board=board)))
    if request.method == "POST":
        user_input = parse_input()
        # check for magic return value of reset button to reset game
        if user_input == 132:
            board = chess.Board()
            return render_template('index.html', svg=Markup(chess.svg.board(board=board)))
        # Save return value. Thus only one function call is necessary
        do_user_move_ret = do_user_move(user_input)
        if do_user_move_ret != 1:
            return do_user_move_ret
        # Save return value. Thus only one function call is necessary
        do_ai_move_ret = do_ai_move()
        if do_ai_move_ret != 1:
            return do_ai_move_ret
        return render_template('index.html', svg=Markup(chess.svg.board(board=board)))

if __name__ == "__main__":
    app.run(debug=False)