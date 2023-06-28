# coding: utf-8

#　必要なモジュールのインポート
from flask import Flask, request, render_template, session, redirect, url_for
from src.game_logic import Player, HumanPlayer, Game
import pickle

# app という変数でFlaskオブジェクトをインスタンス化
app = Flask(__name__)
app.secret_key = "your secret key"


# --- View側の設定 ---

# ルートディレクトリにアクセスした場合の挙動
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 新しいゲームを開始
        player1 = HumanPlayer("Human", 2)
        player2 = Player("Computer", 2)
        game = Game(player1, player2)

        # ゲームの状態をセッションに保存
        session['game'] = pickle.dumps(game)
        session['game_log'] = []
        
        # ゲーム画面にリダイレクト
        return redirect(url_for('input'))
    
    # 初期画面を表示
    return render_template('index.html')

# playerがHumanの場合の、任意の数字を入力する画面
@app.route('/input', methods=['GET', 'POST'])
def input():
    game = pickle.loads(session['game'])
    print(game.total_game_log)  # デバッグ用にゲームログを出力

    # 現在の親プレイヤーがユーザーなら、その call メソッドをユーザーの入力に設定
    if isinstance(game.players[game.current_parent], HumanPlayer):
        if request.method == 'POST':
            user_call = request.form['call']
            game.players[game.current_parent].set_call(int(user_call))
            game_log = game.play_turn()
            session['game'] = pickle.dumps(game)
            session['game_log'] = game_log
            return redirect(url_for('game'))
        else:
            return render_template('input.html', game=game)
    
    # 現在の親プレイヤーがコンピュータなら、その call メソッドを自動生成に設定
    elif isinstance(game.players[game.current_parent], Player):  # ComputerPlayerを示す
        limit = sum([player.life for player in game.players])
        game.players[game.current_parent].set_call(game.players[game.current_parent].call(limit))
        game_log = game.play_turn()
        session['game'] = pickle.dumps(game)
        session['game_log'] = game_log
        return redirect(url_for('game'))
    
    return render_template('input2.html', game=game)




# playerがComputerPlayerの場合の、任意の数字を入力する画面
@app.route('/input2', methods=['GET'])
def input2():
    game = pickle.loads(session['game'])
    print(game.total_game_log)  # デバッグ用にゲームログを出力

    # 現在の親プレイヤーがコンピュータなら、その call メソッドを自動生成に設定し、ターンを進行させる
    if isinstance(game.players[game.current_parent], Player):  # ComputerPlayerを示す
        game.players[game.current_parent].set_call(game.players[game.current_parent].call(game.players[game.current_parent].life))
        game_log = game.play_turn()
        session['game'] = pickle.dumps(game)
        session['game_log'] = game_log

    # ゲームの結果を表示
    return render_template('input2.html', game=game)


# 1ターンのゲームの結果を表示する画面
@app.route('/game', methods=['GET'])
def game():
    default_game_object = pickle.dumps(Game(HumanPlayer("You", 10), Player("Computer", 10)))

    game = pickle.loads(session.get('game', default_game_object))
    game_turn_log = session.get('game_turn_log', [])
    game_log = session.get('game_log', '')

    # ライフが0になったら結果画面にリダイレクト
    if game.is_game_over():
        # game.winner = [player for player in game.players if player.life == 0][0]
        # game.game_log = game_log
        
        # # 更新したゲームの状態をセッションに保存
        # session['game'] = pickle.dumps(game)
        
        return redirect(url_for('result'))
    
    # current_parentを文字列として取得
    current_parent = type(game.players[game.current_parent]).__name__

    # 現在の親プレイヤーがHumanなら、input2画面にリダイレクト
    if isinstance(game.players[game.current_parent], HumanPlayer):
        next_url = url_for('input2')

    # 現在の親プレイヤーがComputerなら、input画面にリダイレクト
    else:
        next_url = url_for('input')

    # ゲームの結果を表示
    return render_template('game.html', game=game, game_turn_log=game.total_game_log, game_log=game_log, turn_count=game.turn_count, next_url=next_url, current_parent=current_parent)


# ゲームの最終結果を表示する画面
@app.route('/result', methods=['GET'])
def result():
    game = pickle.loads(session['game'])

    # ゲームの最終結果を表示
    return render_template('result.html', game=game, winner=game.winner.name, game_log=game.total_game_log)


if __name__ == '__main__':
    app.run(debug=True)