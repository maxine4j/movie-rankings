import sqlite3

db_file = "../data.db"
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
            CREATE TABLE IF NOT EXISTS favourites (
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
    db.execute('''
            CREATE TABLE IF NOT EXISTS polls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creator_user_id INTEGER NOT NULL,
                title TEXT,
                description TEXT,
                
                CONSTRAINT fk_users
                FOREIGN KEY (creator_user_id)
                REFERENCES users (id)
            );
        ''')
    db.execute('''
            CREATE TABLE IF NOT EXISTS poll_choices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                poll_id INTEGER,
                movie_id INTEGER,
                
                UNIQUE(poll_id, movie_id) ON CONFLICT FAIL
                
                CONSTRAINT fk_polls
                FOREIGN KEY (poll_id)
                REFERENCES polls (id),
                
                CONSTRAINT fk_movies
                FOREIGN KEY (movie_id)
                REFERENCES movies (id)
            );
        ''')
    db.execute('''
                CREATE TABLE IF NOT EXISTS poll_votes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    poll_id INTEGER,
                    choice_id INTEGER,
                    user_id INTEGER,

                    UNIQUE(poll_id, user_id) ON CONFLICT REPLACE

                    CONSTRAINT fk_polls
                    FOREIGN KEY (poll_id)
                    REFERENCES polls (id),

                    CONSTRAINT fk_poll_choices
                    FOREIGN KEY (choice_id)
                    REFERENCES poll_choices (id)
                    
                    CONSTRAINT fk_users
                    FOREIGN KEY (user_id)
                    REFERENCES users (id)
                );
            ''')
    db.commit()


def build_user(sql_user):
    # build a user dict from the supplied query result
    return {
        'id': sql_user[0],
        'name': sql_user[1],
    }


def get_user(user_id):
    # returns a dict representing the user with the supplied id
    cur = db.cursor()
    cur.execute('''
        SELECT * FROM users WHERE id = ? LIMIT 1;
        ''', [user_id])
    res = cur.fetchone()
    if res is None:
        return None
    return build_user(res)


def register_user(facebook_id, facebook_name):
    # registers a new facebook user
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


def change_poll_vote(user_id, poll_id, choice_id):
    # adds or changes vote for a given poll/user
    cur = db.cursor()
    cur.execute('''
            INSERT OR REPLACE INTO poll_votes(poll_id, choice_id, user_id)
            VALUES (?, ?, ?);
            ''', [poll_id, choice_id, user_id])
    db.commit()


def build_poll_dicts(sql_res, current_user_id=None):
    # build poll dicts
    polls = {}
    for r in sql_res:
        poll_id = r[0]
        polls[poll_id] = {
            'id': poll_id,
            'creator_user_id': r[1],
            'creator_name': r[7],
            'title': r[2],
            'description': r[3],
            'max_vote_count': 0,
            'total_vote_count': 0,
            'choices': {},
        }
    # populate poll dicts with their choices
    for r in sql_res:
        poll_id = r[0]
        poll_choice_id = r[4]
        vote_count = r[6]
        if not vote_count:
            vote_count = 0
        if polls[poll_id]['max_vote_count'] < vote_count:
            polls[poll_id]['max_vote_count'] = vote_count
        polls[poll_id]['total_vote_count'] += vote_count
        polls[poll_id]['choices'][poll_choice_id] = {
            'id': poll_choice_id,
            'vote_count': vote_count,
            'movie': {
                'id': r[5],
                'title': r[9],
                'release_date': r[10],
                'year': r[10].split('-')[0],
                'overview': r[11],
                'language': r[12],
                'poster_url': r[13],
                'backdrop_url': r[14],
                'genre_ids': r[15],
                'vote_count': r[16],
                'vote_average': r[17],
                'popularity': r[18],
            },
        }
    # flag the choices the logged in user has voted for
    if current_user_id:
        cur = db.cursor()
        cur.execute('''
                SELECT * FROM poll_votes WHERE user_id = ?;
            ''', [current_user_id])
        for r in cur.fetchall():
            poll_id = r[1]
            choice_id = r[2]
            if poll_id in polls:
                polls[poll_id]['choices'][choice_id]['user_voted'] = True
                polls[poll_id]['selected_choice_id'] = choice_id
    return polls


def get_poll(poll_id, current_user_id=None):
    cur = db.cursor()
    sql = '''
        SELECT polls.id AS poll_id, polls.creator_user_id, polls.title, polls.description, 
        poll_choices.id AS choice_id, poll_choices.movie_id AS movie_id,
        cnt.vote_count,
        users.name,
        movies.*
        FROM polls
        LEFT JOIN poll_choices ON polls.id = poll_choices.poll_id
        LEFT JOIN (
            SELECT choice_id, COUNT(*) AS vote_count
            FROM poll_votes
            GROUP BY poll_votes.choice_id
        ) AS cnt ON cnt.choice_id = poll_choices.id
        LEFT JOIN movies ON poll_choices.movie_id = movies.id
        JOIN users ON users.id = polls.creator_user_id
        WHERE poll_id = ?;
    '''
    cur.execute(sql, [poll_id])
    res = cur.fetchall()
    polls = build_poll_dicts(res, current_user_id=current_user_id)
    polls = list(polls.values())
    if len(polls) == 1:
        return polls[0]
    else:
        return None


def get_polls(current_user_id=None, target_user_id=None):
    cur = db.cursor()
    # selects every choice in the db with full movie/poll/vote data
    sql = '''
        SELECT polls.id AS poll_id, polls.creator_user_id, polls.title, polls.description, 
        poll_choices.id AS choice_id, poll_choices.movie_id AS movie_id,
        cnt.vote_count,
        users.name,
        movies.*
        FROM polls
        LEFT JOIN poll_choices ON polls.id = poll_choices.poll_id
        LEFT JOIN (
            SELECT choice_id, COUNT(*) AS vote_count
            FROM poll_votes
            GROUP BY poll_votes.choice_id
        ) AS cnt ON cnt.choice_id = poll_choices.id
        LEFT JOIN movies ON poll_choices.movie_id = movies.id
        JOIN users ON users.id = polls.creator_user_id
    '''
    if target_user_id:
        sql += " WHERE polls.creator_user_id = ?;"
        cur.execute(sql, [target_user_id])
    else:
        sql += ';'
        cur.execute(sql)
    res = cur.fetchall()
    polls = build_poll_dicts(res, current_user_id=current_user_id)
    return list(polls.values())


def add_favourite(user_id, movie_id):
    # adds a favourite for a given movie/user
    cur = db.cursor()
    cur.execute('''
        INSERT OR REPLACE INTO favourites(user_id, movie_id)
        VALUES (?, ?);
        ''', [user_id, movie_id])
    db.commit()


def remove_favourite(user_id, movie_id):
    # removes a favourite for a given movie/user
    cur = db.cursor()
    cur.execute('''
        DELETE FROM favourites
        WHERE user_id = ? AND movie_id = ?;
        ''', [user_id, movie_id])
    db.commit()


def toggle_favourite(user_id, movie_id):
    # toggles a favourite for a given movie/user
    cur = db.cursor()
    cur.execute('SELECT * FROM favourites WHERE movie_id = ? AND user_id = ? LIMIT 1;', [movie_id, user_id])
    res = cur.fetchone()
    if res:
        remove_favourite(user_id, movie_id)
        return False
    else:
        add_favourite(user_id, movie_id)
        return True


def get_fav_movies(user_id):
    # returns all movies favourited by the given user id
    fav_movies = []
    if user_id is not None:
        cur = db.cursor()
        cur.execute('''
                SELECT *
                FROM movies JOIN favourites ON movies.id = favourites.movie_id 
                WHERE favourites.user_id = ?;
                ''', [user_id])
        for x in cur.fetchall():
            fav_movies.append(build_movie(x, False))
    return fav_movies


def add_fav_count(movies):
    cur = db.cursor()
    for m in movies:
        cur.execute('''
            SELECT COUNT(*) as fav_count
            FROM favourites WHERE movie_id = ?
            GROUP BY favourites.movie_id ;
        ''', [m['id']])
        res = cur.fetchone()
        if res:
            m['fav_count'] = res[0]
    return movies


def flag_fav_movies(movies, current_user_id=None):
    # adds a flag to each movie dict in the list movies indicating whether the current user has favourited each movie
    # used to set initial state of favourite/remove favourite button on movie cards
    user_favs = get_fav_movies(current_user_id)
    for movie in movies:
        movie['favourite'] = False
        for fav in user_favs:
            if fav['id'] == movie['id']:
                movie['favourite'] = True
                break
    return movies


def build_movie(sql_movie, has_fav_count=True):
    # builds a movie dict from query results
    movie = {
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
    if has_fav_count:
        movie['fav_count'] = sql_movie[11]
    return movie


def build_movie_list(sql_movies, current_user_id=None):
    # builds a list of movie dicts from query results
    movies = []
    for res in sql_movies:
        movies.append(build_movie(res))
    return flag_fav_movies(movies, current_user_id)


def search_movies(terms, current_user_id=None):
    # searches movies by title using SQL LIKE on each term
    sql = '''
        SELECT movies.*, COUNT(favourites.movie_id) as fav_count 
        FROM movies LEFT JOIN favourites ON movies.id = favourites.movie_id
        WHERE title LIKE ? 
        '''
    if len(terms) > 1:
        for i in range(len(terms) - 1):
            sql += 'AND title LIKE ? '
    sql += '''
        GROUP BY movies.id
        ORDER BY popularity DESC
        LIMIT 50;
    '''
    cur = db.cursor()
    for i in range(len(terms)):
        terms[i] = '%' + terms[i] + '%'
    cur.execute(sql, terms)
    return build_movie_list(cur.fetchall(), current_user_id)


def get_top_favourited_movies(current_user_id=None):
    # returns the top favourited movies by our users
    cur = db.cursor()
    cur.execute('''
        SELECT movies.*, COUNT(favourites.movie_id) as fav_count 
        FROM movies LEFT JOIN favourites ON movies.id = favourites.movie_id
        GROUP BY movies.id
        ORDER BY fav_count DESC, vote_count / 1000 * vote_average DESC
        LIMIT 50;
        ''')
    return build_movie_list(cur.fetchall(), current_user_id)


def get_popular_movies(current_user_id=None):
    # returns the most popular movies according to our data source "the movie database"
    cur = db.cursor()
    cur.execute('''
        SELECT movies.*, COUNT(favourites.movie_id) as fav_count 
        FROM movies LEFT JOIN favourites ON movies.id = favourites.movie_id
        GROUP BY movies.id
        ORDER BY popularity DESC
        LIMIT 50;
        ''')
    return build_movie_list(cur.fetchall(), current_user_id)


def get_all_movies():
    cur = db.cursor()
    cur.execute('SELECT *, "null" FROM movies;')
    return build_movie_list(cur.fetchall())


def create_poll(cur_user_id, title, desc, choice_movie_ids):
    cur = db.cursor()
    # create the poll
    cur.execute('''
        INSERT INTO polls(
        creator_user_id,
        title,
        description)
        VALUES(?, ?, ?);
    ''', [cur_user_id, title, desc])
    poll_id = cur.lastrowid
    # create the choices for the poll
    for mid in choice_movie_ids:
        cur.execute('''
            INSERT INTO poll_choices(
            poll_id,
            movie_id)
            VALUES(?, ?);
        ''', [poll_id, mid])
