from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST' and request.form['username']:
        plr_username = request.form['username']
        game1 = request.form['game1']
        game2 = request.form['game2']
    return render_template('add_player.html')


if __name__ == "__main__":
    app.run(debug=True)