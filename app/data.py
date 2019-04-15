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


def get_user_fav_movies(user_id):
    cur = db.cursor()
    cur.execute('''
        SELECT * FROM movies JOIN votes ON movies.id = votes.movie_id WHERE votes.user_id = ?;
        ''', [user_id])
    all_res = cur.fetchall()
    movies = []
    for res in all_res:
        movie = build_movie(res)
        movies.append(movie)
    return movies


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


def remove_vote(user_id, movie_id):
    cur = db.cursor()
    cur.execute('''
        DELETE FROM votes
        WHERE user_id = ? AND movie_id = ?;
        ''', [user_id, movie_id])
    db.commit()


def toggle_vote(user_id, movie_id):
    cur = db.cursor()
    cur.execute('SELECT * FROM votes WHERE movie_id = ? AND user_id = ? LIMIT 1;', [movie_id, user_id])
    res = cur.fetchone()
    if res:
        remove_vote(user_id, movie_id)
        return False
    else:
        add_vote(user_id, movie_id)
        return True


def build_movie(sql_movie):
    return {
        'id': sql_movie[0],
        'title': sql_movie[1],
        'release_date': sql_movie[2],
        'year': sql_movie[2].split('-')[0],
        'overview': sql_movie[3],
        'language': sql_movie[4],
        'poster_url': sql_movie[5],
        'backdrop_url': sql_movie[6],
        'genre_ids': sql_movie[7],
        'vote_count': sql_movie[8],
        'vote_average': sql_movie[9],
        'popularity': sql_movie[10],
    }


def prepare_movie_list(movies, current_user_id):
    # marks movies as favourited for the logged in user
    user_favs = get_user_fav_movies(current_user_id)
    for movie in movies:
        movie['favourite'] = False
        for fav in user_favs:
            if fav['id'] == movie['id']:
                movie['favourite'] = True
                break
    return movies


def build_movie_list(sql_movies):
    movies = []
    for res in sql_movies:
        movies.append(build_movie(res))
    return movies


def search_movies(terms):
    sql = 'SELECT * FROM movies WHERE title LIKE ? '
    if len(terms) > 1:
        for i in range(len(terms) - 1):
            sql += 'AND title LIKE ? '
    sql += 'LIMIT 50;'
    cur = db.cursor()
    for i in range(len(terms)):
        terms[i] = '%' + terms[i] + '%'
    cur.execute(sql, terms)
    return build_movie_list(cur.fetchall())


def get_all_movies():
    cur = db.cursor()
    cur.execute('''
        SELECT * FROM movies;
        ''')
    return build_movie_list(cur.fetchall())

