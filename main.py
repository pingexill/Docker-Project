from flask import Flask, request, render_template, redirect, url_for
import _sqlite3, os

# docker volume create game-data
# docker build -t exam .
# docker run -p 5000:5000 -v game-data:/app/data exam

# git add <file_name>
# git commit --amend --no-edit
# git commit -m "message"
# git push
# git push --force

app = Flask(__name__)

DATABASE_FOLDER = "data"
DATABASE_PATH = f"{DATABASE_FOLDER}/data.db"

def get_connection():
    os.makedirs(DATABASE_FOLDER, exist_ok=True)
    conn = _sqlite3.connect(DATABASE_PATH)
    conn.row_factory = _sqlite3.Row

    return conn
   
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS games(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT NOT NULL, 
            genre TEXT NOT NULL, 
            platform TEXT NOT NULL,
            rating TEXT NOT NULL,
            description TEXT,
            release_year INTEGER NOT NULL
            )""")
    conn.commit()
    conn.close()



@app.route('/')
def  home():
    return render_template('welcome_page.html')


@app.route('/game_list', methods=['GET']) # Commit 2
def game_list():
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM games"
    conditions = []
    parameters = []

    name = request.args.get('name-search', '').strip()
    genre = request.args.get('genre-search', '').strip()
    platform = request.args.get('platform-search', '').strip()
    rating = request.args.get('rating-search', '').strip()
    year = request.args.get('year-search', '').strip()

    if name:
        conditions.append("title LIKE ?")
        parameters.append(f"%{name}%")
    
    if genre:
        conditions.append("genre LIKE ?")
        parameters.append(f"%{genre}%")

    if platform:
        conditions.append("platform LIKE ?")
        parameters.append(f"%{platform}%")

    if rating:
        conditions.append("rating >= ?") 
        parameters.append(float(rating))

    if year:
        conditions.append("release_year = ?")
        parameters.append(int(year))

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, tuple(parameters))
    games = cursor.fetchall()
    conn.close()

    return render_template('game_list.html', games=games, search_values={
        'name': name, 'genre': genre, 'platform': platform, 'rating': rating, 'year': year
    })


@app.route('/game/<int:game_id>') # Commit 2
def  game_detail(game_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))
    game = cursor.fetchone()
    conn.close()
    
    if game is None:
        return "Game not found", 404
    return render_template('game.html', game=game)


@app.route('/add_game', methods=['GET', 'POST']) # Commit 2
def  add_game():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        platform = request.form['platform']
        rating = request.form['rating']
        description = request.form['description']
        release_year = request.form['release_year']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO games (title, genre, platform, rating, description, year)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, genre, platform, rating, description, release_year))
        conn.commit()
        conn.close()

        return redirect(url_for('game_list'))

    return render_template('add_game.html')


@app.route('/recommend_game', methods=['GET', 'POST'])
def  recommend_game():
    return render_template('recommend_game.html')



if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=5000)