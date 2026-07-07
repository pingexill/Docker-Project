from flask import Flask, request, render_template, redirect, url_for
import _sqlite3, os, random

# docker volume create games-data
# docker build -t exam .
# docker run -p 5000:5000 -v games-data:/app/data exam

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
            release_year INTEGER NOT NULL,
            image_url TEXT,
            creator TEXT NOT NULL,
            price TEXT NOT NULL
            )""") #New column added: image_url, creator, price
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

    creator = request.args.get('creator-search', '').strip()
    price = request.args.get('price-search', '').strip()

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


    if creator:
        conditions.append("creator LIKE ?")
        parameters.append(f"%{creator}%")

    if price:
        conditions.append("price LIKE ?")
        parameters.append(f"%{price}%")


    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, tuple(parameters))
    games = cursor.fetchall()
    conn.close()

    return render_template('game_list.html', games=games, search_values={
        'name': name, 'genre': genre, 'platform': platform, 'rating': rating, 'year': year, 'creator': creator, 'price': price
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

@app.route('/delete_game/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM games WHERE id = ?", (game_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('game_list'))

@app.route('/add_game', methods=['GET', 'POST']) # Commit 2
def  add_game():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        platform = request.form['platform']
        rating = request.form['rating']
        description = request.form['description']
        release_year = request.form['release_year']
        # New fields added for image_url, creator, and price
        image_url = request.form['image_url']
        creator = request.form['creator']
        price = request.form['price']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO games (title, genre, platform, rating, description, release_year, image_url, creator, price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, genre, platform, rating, description, release_year,     image_url, creator, price))
        conn.commit()
        conn.close()

        return redirect(url_for('game_list'))

    return render_template('add_game.html')


@app.route('/recommend_game', methods=['GET', 'POST'])
def  recommend_game():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()

    rand = random.randint(1, len(games))
    game = games[rand - 1]

    return render_template('recommend_game.html', game=game)

@app.route('/statistics', methods=['GET'])
def  statistics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT genre, COUNT(*) as count FROM games GROUP BY genre")
    genre_stats = cursor.fetchall()

    cursor.execute("SELECT platform, COUNT(*) as count FROM games GROUP BY platform")
    platform_stats = cursor.fetchall()

    cursor.execute("SELECT rating, COUNT(*) as count FROM games GROUP BY rating")
    rating_stats = cursor.fetchall()


    cursor.execute("SELECT COUNT(*) FROM games")
    total_games = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(rating) as average_rating FROM games")
    average_rating = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM games WHERE rating = (SELECT MIN(rating) FROM games)")
    min_rating = cursor.fetchone()

    cursor.execute("SELECT * FROM games WHERE rating = (SELECT MAX(rating) FROM games)")
    max_rating = cursor.fetchone()

    cursor.execute("SELECT * FROM games WHERE release_year = (SELECT MIN(release_year) FROM games)")
    min_year = cursor.fetchone()

    cursor.execute("SELECT * FROM games WHERE release_year = (SELECT MAX(release_year) FROM games)")
    max_year = cursor.fetchone()


    conn.close()

    return render_template('statistics.html', genre_stats=genre_stats, platform_stats=platform_stats, rating_stats=rating_stats, average_rating=average_rating, total_games=total_games, min_year=min_year, max_year=max_year, min_rating=min_rating, max_rating=max_rating)

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=5000)