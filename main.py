from flask import Flask, request, render_template, redirect, url_for
import _sqlite3, os

# docker volume create game-data
# docker build -t exam .
# docker run -p 5000:5000 -v game-data:/app/data exam

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
            year INTEGER NOT NULL
            )""")
    conn.commit()
    conn.close()



@app.route('/')
def  home():
    return render_template('welcome_page.html')


@app.route('/game_list')
def  game_list():
    return render_template('game_list.html')


@app.route('/game/<int:game_id>')
def  game_detail(game_id):
    return render_template('game_detail.html', game_id=game_id)


@app.route('/add_game', methods=['GET', 'POST'])
def  add_game():
    return render_template('add_game.html')


@app.route('/recommend_game', methods=['GET', 'POST'])
def  recommend_game():
    return render_template('recommend_game.html')



if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=5000)