import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('track-achievs', check_same_thread=False)
        self.cur = self.conn.cursor()

        self.cur.execute('CREATE TABLE IF NOT EXISTS players (username, game_list)')
        self.cur.execute('CREATE TABLE IF NOT EXISTS achievements (title, game, player_id)')
        self.conn.commit()

    def add_player(self, user, games):
        task = 'INSERT INTO players (username, game_list) VALUES (?, ?)'
        if len(games) > 1:
            plr_games = ''
            for game in games:
                plr_games += f'{game} '
        else:
            plr_games = games[0]
        self.cur.execute(task, (user, plr_games,))
        self.conn.commit()
    
    def add_achievement(self, title, game, player_id):
        task = 'INSERT INTO achievements (title, game, player_id) VALUES (?, ?, ?)'
        self.cur.execute(task, (title, game, player_id,))
        self.conn.commit()
        
