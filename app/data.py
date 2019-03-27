import sqlite3

db_file = "data.db"

'''
{
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
  "Poster": "https:\/\/m.media-amazon.com\/images\/M\/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
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
'''

def init_db():
    db = sqlite3.connect(db_file)
    db.execute('''
    CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT, 
            year INTEGER,
            rating TEXT,
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
