import sqlite3

db_file = "C:\\Dev\\repo\\CITS3403-Project1-SocialChoice\\data.db"
db = sqlite3.connect(db_file, check_same_thread=False)

godfather_obj = {
  "Title": "The Godfather",
  "Year": "1972",
  "Rated": "R",
  "Released": "24 Mar 1972",
  "Runtime": "175 min",
  "Genre": "Crime, Drama",
  "Director": "Francis Ford Coppola",
  "Writer": "Mario Puzo (screenplay by), Francis Ford Coppola (screenplay by), Mario Puzo (based on the novel by)",
  "Actors": "Marlon Brando, Al Pacino, James Caan, Richard S. Castellano",
  "Plot": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
  "Language": "English, Italian, Latin",
  "Country": "USA",
  "Awards": "Won 3 Oscars. Another 24 wins & 28 nominations.",
  "Poster": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
  "Ratings": [
    {
      "Source": "Internet Movie Database",
      "Value": "9.2\/10"
    },
    {
      "Source": "Metacritic",
      "Value": "100\/100"
    }
  ],
  "Metascore": "100",
  "imdbRating": "9.2",
  "imdbVotes": "1,417,421",
  "imdbID": "tt0068646",
  "Type": "movie",
  "DVD": "09 Oct 2001",
  "BoxOffice": "N\/A",
  "Production": "Paramount Pictures",
  "Website": "http:\/\/www.thegodfather.com",
  "Response": "True"
}


def init_db():
    print('init db called!')
    db.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT, 
            year INTEGER,
            rated TEXT,
            release_date TEXT,
            runtime INTEGER,
            genre TEXT,
            director TEXT,
            writer TEXT,
            actors TEXT,
            plot TEXT,
            language TEXT,
            country TEXT,
            awards TEXT,
            poster_url TEXT,
            metascore INTEGER,
            imdb_rating INTEGER,
            imdb_votes INTEGER,
            imdb_id TEXT,
            type TEXT,
            dvd_release TEXT,
            box_office TEXT,
            production TEXT,
            website TEXT
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


def add_vote(user_token, movie_id):
    cur = db.cursor()
    cur.execute('''
        INSERT OR REPLACE INTO votes(user_id, movie_id)
        VALUES (?, ?);
        ''', [user_token, movie_id])
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
            'year': res[2],
            'rating': res[3],
            'release_date': res[4],
            'runtime': res[5],
            'genre': res[6],
            'director': res[7],
            'writer': res[8],
            'actors': res[9],
            'plot': res[10],
            'language': res[11],
            'country': res[12],
            'awards': res[13],
            'poster_url': res[14],
            'metascore': res[15],
            'imdb_rating': res[16],
            'imdb_votes': res[17],
            'imdb_id': res[18],
            'type': res[19],
            'dvd_release': res[20],
            'box_office': res[21],
            'production': res[22],
            'website': res[23],
        })
    return movies


def insert_test_data():
    init_db()
    for i in range(200):
        db.execute('''
            INSERT INTO movies(
            title, 
            year,
            rated,
            release_date,
            runtime,
            genre,
            director,
            writer,
            actors,
            plot,
            language,
            country,
            awards,
            poster_url,
            metascore,
            imdb_rating,
            imdb_votes,
            imdb_id,
            type,
            dvd_release,
            box_office,
            production,
            website)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
            ''', [
                    godfather_obj['Title'],
                    godfather_obj['Year'],
                    godfather_obj['Rated'],
                    godfather_obj['Released'],
                    godfather_obj['Runtime'],
                    godfather_obj['Genre'],
                    godfather_obj['Director'],
                    godfather_obj['Writer'],
                    godfather_obj['Actors'],
                    godfather_obj['Plot'],
                    godfather_obj['Language'],
                    godfather_obj['Country'],
                    godfather_obj['Awards'],
                    godfather_obj['Poster'],
                    godfather_obj['Metascore'],
                    godfather_obj['imdbRating'],
                    godfather_obj['imdbVotes'],
                    godfather_obj['imdbID'],
                    godfather_obj['Type'],
                    godfather_obj['DVD'],
                    godfather_obj['BoxOffice'],
                    godfather_obj['Production'],
                    godfather_obj['Website']
                ])
    db.commit()

#insert_test_data()
