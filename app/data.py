import sqlite3

db_file = "C:\\Dev\\repo\\CITS3403-Project1-SocialChoice\\data.db"
db = sqlite3.connect(db_file, check_same_thread=False)


def init_db():
    db.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY, 
            title TEXT, 
            release_date TEXT,
            overview TEXT,
            language TEXT,
            poster_url TEXT,
            backdrop_url TEXT,
            genre_ids INTEGER,
            vote_count INTEGER,
            vote_average REAL,
            popularity REAL
        );
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT
        );
    ''')
    db.execute('''
            CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            movie_id INTEGER,
            
            UNIQUE(user_id, movie_id) ON CONFLICT FAIL
            
            CONSTRAINT fk_users
            FOREIGN KEY (user_id)
            REFERENCES users (id),
            
            CONSTRAINT fk_movies
            FOREIGN KEY (movie_id)
            REFERENCES movies (id)
        );
    ''')
    db.commit()


def get_user(user_id):
    cur = db.cursor()
    cur.execute('''
        SELECT * FROM users WHERE id = ? LIMIT 1;
        ''', [user_id])
    return cur.fetchone()


def register_user(facebook_id, facebook_name):
    cur = db.cursor()
    try:
        cur.execute('''
            INSERT INTO users(id, name)
            VALUES (?, ?);
            ''', [facebook_id, facebook_name])
        db.commit()
        return True, 'User registered successfully'
    except sqlite3.IntegrityError:
        return False, 'User already registered'


def get_vote_count(movie_id):
    cur = db.cursor()
    cur.execute('''
        SELECT COUNT(*) FROM votes
        WHERE movie_id = ?;
        ''', [movie_id])


def add_vote(user_id, movie_id):
    cur = db.cursor()
    cur.execute('''
        INSERT OR REPLACE INTO votes(user_id, movie_id)
        VALUES (?, ?);
        ''', [user_id, movie_id])
    db.commit()
    return True, 'Successfully added vote'


def remove_vote(user_token, movie_id):
    cur = db.cursor()
    cur.execute('''
        DELETE FROM votes
        WHERE user_id = ? AND movie_id = ? LIMIT 1;
        ''', [user_token, movie_id])
    db.commit()


def get_all_movies():
    cur = db.cursor()
    cur.execute('''
        SELECT * FROM movies;
        ''')
    all_res = cur.fetchall()
    movies = []
    for res in all_res:
        movies.append({
            'id': res[0],
            'title': res[1],
            'release_date': res[2],
            'year': res[2].split('-')[0],
            'overview': res[3],
            'language': res[4],
            'poster_url': res[5],
            'backdrop_url': res[6],
            'genre_ids': res[7],
            'vote_count': res[8],
            'vote_average': res[9],
            'popularity': res[10],
        })
    return movies
