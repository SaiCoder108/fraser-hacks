from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    time_spent INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

# Update time spent by a user
@app.route('/update-time', methods=['POST'])
def update_time():
    data = request.json
    time_spent = data['timeSpent']
    # Assume the user's name is passed in the session or as an identifier
    user_name = "Default User"

    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO leaderboard (name, time_spent) 
        VALUES (?, ?)
        ON CONFLICT(name) DO UPDATE SET time_spent = time_spent + ?;
    ''', (user_name, time_spent, time_spent))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

# Render leaderboard
@app.route('/leaderboard')
def leaderboard():
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()
    c.execute('SELECT name, time_spent FROM leaderboard ORDER BY time_spent DESC')
    leaderboard_data = c.fetchall()
    conn.close()
    return render_template('leaderboard.html', leaderboard=leaderboard_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
