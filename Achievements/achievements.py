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

        tracker.add_player(plr_username, [game1, game2])
        return redirect(url_for('view_player_data'))
    return render_template('add_player.html')

# database testing
@app.route('/player-data')
def view_player_data():
    data = tracker.cur.execute('SELECT * FROM players').fetchall()
    return render_template('player_data.html', data=data, cur_amount=len(data))

@app.route('/track-achievement', defaults={'user_id':None})
@app.route('/track-achievement/<int:user_id>', methods=['GET', 'POST'])
def track_achiev(user_id):
    if user_id is None:
        message='Choose the player first'
        flash(message)
        data = tracker.cur.execute('SELECT * FROM players').fetchall()
        return render_template('player_data.html', data=data, cur_amount=len(data))
    else:
        user = tracker.cur.execute('SELECT * FROM players WHERE player_id=?', (user_id,)).fetchone()

        if request.method == 'POST' and request.form['game'] and request.form['title']:
            game = request.form['game']
            title = request.form['title']

            tracker.add_achievement(title, game, user_id)
            flash(f'Achievement added for {user[0]}')
            return redirect(url_for('view_player_data'))

        return render_template('track_achievement.html', user=user)

@app.route('/delete-user/<int:user_id>', methods=['POST', 'GET'])
def delete_user_route(user_id):
    delete_user(user_id)
    return redirect(url_for('view_player_data'))

@app.route('/view-achievements/<int:user_id>', methods=['GET'])
def view_achievs(user_id):
    user = tracker.conn.execute('SELECT * FROM players WHERE player_id = ?', (user_id,)).fetchone()
    task = 'SELECT * FROM achievements WHERE player_id = ?'
    user_achievs = tracker.cur.execute(task, (user_id,)).fetchall()
    print(user_achievs)
    return render_template('player_achievements.html', user=user, achievs=user_achievs, cur_amount=len(user_achievs))

def delete_user(user_id):
    message = f"Deleting user with id {user_id}"
    tracker.cur.execute('DELETE FROM players WHERE player_id = ?', (user_id,))
    tracker.cur.execute('DELETE FROM achievements WHERE player_id = ?', (user_id,))
    tracker.conn.commit()

if __name__ == "__main__":
    app.run(debug=True)