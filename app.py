from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session tracking

# Database setup
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS leaderboard (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            school TEXT NOT NULL,
                            email TEXT NOT NULL,
                            points INTEGER NOT NULL
                        )''')

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        school = request.form['school']
        email = request.form['email']
        
        # Calculate points based on time spent
        if 'start_time' in session:
            session_duration = time.time() - session['start_time']
            points = int(session_duration)  # Points based on seconds spent
        else:
            points = 0
        
        # Save to database
        with sqlite3.connect('database.db') as conn:
            conn.execute("INSERT INTO leaderboard (name, school, email, points) VALUES (?, ?, ?, ?)", 
                         (name, school, email, points))
        
        # Reset session start time
        session.pop('start_time', None)
        
        return redirect(url_for('leaderboard'))

    # Start tracking time when user visits this page
    session['start_time'] = time.time()
    return render_template('register.html')

@app.route('/leaderboard')
def leaderboard():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.execute("SELECT name, school, email, points FROM leaderboard ORDER BY points DESC")
        data = cursor.fetchall()
    return render_template('leaderboard.html', leaderboard=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
