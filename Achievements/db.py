import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('track-achievs', check_same_thread=False)
        self.cur = self.conn.cursor()

        self.cur.execute('CREATE TABLE IF NOT EXISTS players (player_id INTEGER PRIMARY KEY AUTOINCREMENT, username, game_list)')
        self.cur.execute('CREATE TABLE IF NOT EXISTS achievements (title, game, player_id)')
        self.conn.commit()

    def add_player(self, user, games):
        task = 'INSERT INTO players (username, game_list) VALUES (?, ?)'
        if len(games) > 1:
            plr_games = ''
            for i in range(len(games)):
                if i < len(games)-1:
                    plr_games += f'{games[i]} '
                else:
                    plr_games += f'{games[i]}'
        else:
            plr_games = games[0]
        self.cur.execute(task, (user, plr_games,))
        self.conn.commit()
    
    def add_achievement(self, title, game, player_id):
        task = 'INSERT INTO achievements (title, game, player_id) VALUES (?, ?, ?)'
        self.cur.execute(task, (title, game, player_id,))
        self.conn.commit()

### db tests
if __name__ == '__main__':
    db = DB()

    # print(db.conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    a = db.conn.execute('select * from achievements').fetchall()
    p = db.conn.execute('select * from players').fetchall()
    print()
    print(p)
    print()
    print(a)
    print()
    c = db.conn.execute('SELECT players.username, achievements.game, achievements.title FROM players INNER JOIN achievements ON achievements.player_id=players.player_id').fetchall()
    for i in c:
        print(i)

        
