/*CREATE TABLE movies (
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
);*/
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    name TEXT,
    admin INTEGER DEFAULT 0
);
CREATE TABLE favourites (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users (id) ON DELETE CASCADE,
    movie_id INTEGER REFERENCES movies (id) ON DELETE CASCADE,
    UNIQUE(user_id, movie_id)
);
CREATE TABLE polls (
    id SERIAL PRIMARY KEY,
    creator_user_id BIGINT REFERENCES users (id) ON DELETE CASCADE,
    title TEXT,
    description TEXT
);
CREATE TABLE poll_choices (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER REFERENCES polls (id) ON DELETE CASCADE,
    movie_id INTEGER REFERENCES movies (id) ON DELETE CASCADE,
    UNIQUE(poll_id, movie_id)
);
CREATE TABLE poll_votes (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER REFERENCES polls (id) ON DELETE CASCADE,
    choice_id INTEGER REFERENCES poll_choices (id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES users (id) ON DELETE CASCADE,
    UNIQUE(poll_id, user_id)
);
CREATE TABLE poll_comments (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER REFERENCES polls (id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES users (id) ON DELETE CASCADE,
    body TEXT,
    timestamp INTEGER
);
