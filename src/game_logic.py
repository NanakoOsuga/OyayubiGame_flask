# 必要なライブラリのインポート
import random
from typing import Any

# Player (ComputerPlayer)
class Player:
    def __init__(self, name, life):
        self.name = name
        self.life = life
        self._next_call = None
        self.score = 0
    
    def call(self, limit):
        if self._next_call is None:
            self._next_call = random.randint(0, limit)

        call = self._next_call
        self._next_call = None # 入力をクリア
        return call
    
    def set_call(self, call):
        self._next_call = call

    def lower_life(self):
        if self.life > 0:
            self.life -= 1
            return self.life
        else:
            return 0
        
    def set_score(self):
        self.score = random.randint(0, self.life)
        
# Human
class HumanPlayer(Player):
    def __init__(self, name, life):
        super().__init__(name, life)

    def set_call(self, call):
        self._next_call = call

    def call(self, limit):
        if self._next_call is None:
            self._next_call = random.randint(0,limit)
        
        call = self._next_call
        self._next_call = None  # 入力をクリア
        return call


class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_parent = 0
        self.call_parent = 0
        self.turn_count = 0
        self.current_call = 0
        self.call_parent = 0
        self.call_parent = self.current_parent # 親の値を同期
        self.total_game_log = []  # 全ゲームログをここで収集する
    
    def play_turn(self):
        game_log = []  # このゲームログを各ターンで更新する
        
        # 親の値を同期
        self.call_parent = self.current_parent

        # call_parent = self.current_parent

        # ターンを記録
        self.turn_count += 1
        game_log.append(f"【ターン{self.turn_count}】")
        
        # callの設定
        limit = sum([player.life for player in self.players])
        self.current_call = self.players[self.current_parent].call(limit)
        game_log.append(f"{self.players[self.current_parent].name} が {self.current_call} をコールしました。")
        
        # スコアを設定
        for player in self.players:
            player.set_score()
        scores = [player.score for player in self.players]
        # scores = [random.randint(0,player.life) for player in self.players]
        game_log.append(f"各プレイヤーのスコア: {scores}")
        
        # そのターンでの勝者を出力
        if sum(scores) == self.current_call:
            game_log.append(f"{self.players[self.call_parent].name} の勝利！")
            self.players[self.call_parent].lower_life() #call_parentのlifeを1減らす
        else:
            game_log.append(f"ドロー")
        
        
        # 更新された現在の親を、元に戻す
        self.current_parent = (self.current_parent + 1) % len(self.players)

        # 残りの指の数を出力
        game_log.append(f"残りライフ：{self.players[0].name}は{self.players[0].life}、{self.players[1].name}は{self.players[1].life}")

        # ゲームログに追加
        game_log_str = '\n'.join(game_log)  # リストを改行で結合した一つの文字列に変換
        self.total_game_log.append(game_log_str)  # 全ゲームログにこのターンのログを追加する

        # いずれかのlifeが0になっていれば、最終的な勝者を出力
        for player in self.players:
            if player.life == 0:
                winner_log = f"勝者は {player.name} です！"
                self.total_game_log.append(winner_log)
                self.winner = player
                break

        # print("ターンごとのログ：", self.game_log)

        return '\n'.join(self.total_game_log)  # このゲームログを返す


    # def play_game(self):
        
    #     while all([player.life > 0 for player in self.players]):
    #         self.play_turn() # 各ターンのゲームログを収集する
        
    #     for player in self.players:
    #         if player.life == 0:
    #             winner_log = f"勝者は {player.name} です！"
    #             self.total_game_log.append(winner_log)
    #             self.winner = player
    #             break

    #     print("すべてのログ：", self.total_game_log)

    #     return '\n'.join(self.total_game_log)  # 全ゲームログを一つの文字列に結合して返す
    
    def is_game_over(self):
        game_over =  any([player.life <= 0 for player in self.players])
        if game_over:
            self.total_game_log = []
        return game_over
