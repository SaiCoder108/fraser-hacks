from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS leaderboard (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            score INTEGER NOT NULL
                        )''')

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        score = request.form['score']
        if name and score.isdigit():
            with sqlite3.connect('database.db') as conn:
                conn.execute("INSERT INTO leaderboard (name, score) VALUES (?, ?)", (name, int(score)))
            return redirect(url_for('leaderboard'))
    return render_template('register.html')

@app.route('/leaderboard')
def leaderboard():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.execute("SELECT name, score FROM leaderboard ORDER BY score DESC")
        data = cursor.fetchall()
    return render_template('leaderboard.html', leaderboard=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
