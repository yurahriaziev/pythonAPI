from flask import Flask, render_template, request, url_for, redirect, flash
from db import DB

app = Flask(__name__)
# database variables 'tracker'
tracker = DB()
app.secret_key = "InsaneSecretKey"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST' and request.form['username']:
        plr_username = request.form['username']
        game1 = request.form['game1']
        game2 = request.form['game2']
        password = request.form['password']

        tracker.add_player(plr_username, [game1, game2], password)
        return redirect(url_for('view_player_data'))
    return render_template('add_player.html')


# database testing
@app.route('/player-data')
def view_player_data():
    data = tracker.cur.execute('SELECT rowid, username, game_list FROM players').fetchall()
    print(data)
    return render_template('player_data.html', data=data)

@app.route('/track-achievement', methods=['GET', 'POST'])
def track_achiev():
    return render_template('track-achievement.html')

@app.route('/delete-user/<int:user_id>', methods=['POST', 'GET'])
def delete_user_route(user_id):
    delete_user(user_id)
    return redirect(url_for('view_player_data'))

def delete_user(user_id):
    message = f"Deleting user with id {user_id}"
    tracker.conn.execute('DELETE FROM players WHERE rowid = ?', (user_id,))
    return render_template('player_data.html')

if __name__ == "__main__":
    app.run(debug=True)