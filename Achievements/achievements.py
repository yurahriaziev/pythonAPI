from flask import Flask, render_template, request, url_for, redirect
from db import DB

app = Flask(__name__)
# database variables 'tracker'
tracker = DB()

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
        return redirect(url_for('home'))
    return render_template('add_player.html')


# database testing
@app.route('/player-data')
def view_player_data():
    data = tracker.cur.execute('SELECT * FROM players').fetchall()
    print(data)
    return render_template('player_data.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)