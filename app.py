from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# In-memory leaderboard storage (use a database for production)
leaderboard = {}

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/leaderboard')
def show_leaderboard():
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    return render_template('leaderboard.html', leaderboard=sorted_leaderboard)

@app.route('/update-time', methods=['POST'])
def update_time():
    data = request.get_json()
    name = request.args.get('name', 'Anonymous')  # Get the user's name, default to 'Anonymous'
    time_spent = data.get('timeSpent', 0)

    # Update leaderboard with time spent
    if name in leaderboard:
        leaderboard[name] += time_spent
    else:
        leaderboard[name] = time_spent

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
