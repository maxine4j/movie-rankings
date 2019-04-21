import requests
import sqlite3
import time
import os
import random


def insert_test_users():
    db_file = "C:\\Dev\\repo\\CITS3403-Project1-SocialChoice\\data.db"
    db = sqlite3.connect(db_file, check_same_thread=False)
    movies = [
        238,
        680,
        578,
        694,
        2108,
        274,
        197,
        27205,
    ]
    sql = '''
        insert into users(id, name) VALUES (1,"Alice");
        insert into users(id, name) VALUES (2,"Bob");
        insert into users(id, name) VALUES (3,"Carl");
        insert into users(id, name) VALUES (4,"Dave");
        insert into users(id, name) VALUES (5,"Edd");
        insert into users(id, name) VALUES (6,"Fred");
        insert into users(id, name) VALUES (7,"Gavin");
        insert into users(id, name) VALUES (8,"Harry");
        insert into users(id, name) VALUES (9,"Ilsa");
        insert into users(id, name) VALUES (10,"Jake");
        '''.split('\n')
    print(sql)
    for i in range(100):
        #db.execute('INSERT INTO users(id, name) VALUES (?,?);', [i, i])
        for movie in movies:
            if random.choice([True] + [False] * 5):
                try:
                    db.execute('INSERT INTO votes(user_id, movie_id) VALUES (?,?);', [i, movie])
                    db.commit()
                except:
                    pass
        db.commit()


def build_movie(sql_movie):
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
    }
    return movie


def build_movie_list(sql_movies):
    # builds a list of movie dicts from query results
    movies = []
    for res in sql_movies:
        movies.append(build_movie(res))
    return movies


def build_user(sql_user):
    # build a user dict from the supplied query result
    return {
        'id': sql_user[0],
        'name': sql_user[1],
    }


def build_user_list(sql_users):
    users = []
    for res in sql_users:
        users.append(build_user(res))
    return users


def insert_test_polls():
    db_file = "C:\\Dev\\repo\\CITS3403-Project1-SocialChoice\\data.db"
    db = sqlite3.connect(db_file, check_same_thread=False)
    # get all users and movies
    users = build_user_list(db.execute('SELECT * FROM users;'))
    movies = build_movie_list(db.execute('SELECT * FROM movies;'))
    # add some polls
    li = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent posuere feugiat elit, vitae ultrices arcu consequat ac. Sed ut ipsum tortor. Duis ac aliquam nibh, a mollis enim. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec et venenatis sem. Ut ullamcorper velit nec ex dictum aliquam. Vivamus euismod, felis ut euismod viverra, risus tellus tincidunt massa, eu efficitur magna sapien et felis.'
    for poll_id in range(25, 50):
        db.execute('''
            INSERT INTO polls(
            id,
            creator_user_id,
            title,
            description)
            VALUES(?, ?, ?, ?);
        ''', [poll_id, random.choice(users)['id'], 'POLL_TITLE_' + str(poll_id), li])
        # add some choices for the poll
        for j in range(1, 20):
            if random.choice([True] * 4 + [False]):
                db.execute('''
                    INSERT INTO poll_choices(
                    poll_id,
                    movie_id)
                    VALUES(?, ?);
                ''', [poll_id, random.choice(movies)['id']])
    db.commit()


def insert_test_poll_votes():
    db_file = "C:\\Dev\\repo\\CITS3403-Project1-SocialChoice\\data.db"
    db = sqlite3.connect(db_file, check_same_thread=False)
    # get all users and movies
    res = db.execute('SELECT * FROM users;')
    user_ids = []
    for r in res:
        user_ids.append(r[0])
    res = db.execute('SELECT * FROM poll_choices;')
    poll_choices = []
    for r in res:
        poll_choices.append((r[0], r[1]))
    for i in range(1, 1000):
        pc = random.choice(poll_choices)
        uid = random.choice(user_ids)
        db.execute('''
            INSERT INTO poll_votes(
            poll_id, 
            choice_id, 
            user_id)
            VALUES(?, ?, ?);
        ''', [pc[1], pc[0], uid])
    db.commit()


def update_movie_db():
    db_file = "C:\\Dev\\repo\\CITS3403-Project1-SocialChoice\\data.db"
    db = sqlite3.connect(db_file, check_same_thread=False)
    url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc"
    api_key = os.environ.get('THEMOVIEDB_KEY')
    for i in range(1, 1000):
        time.sleep(0.251)  # rate limit 4 calls per second
        req_url = url + '&api_key=' + api_key + '&page=' + str(i)
        print('Getting page =', i, 'URL =', req_url)
        res = requests.get(req_url)
        if res.ok:
            print('Got Response:', res.status_code, res.reason)
            res_json = res.json()
            print(res_json)
            for movie in res_json['results']:
                db.execute('''
                    INSERT INTO movies(
                    id, 
                    title, 
                    release_date,
                    overview,
                    language,
                    poster_url,
                    backdrop_url,
                    genre_ids,
                    vote_count,
                    vote_average,
                    popularity)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?);
                    ''', [movie['id'],
                          movie['title'],
                          movie['release_date'],
                          movie['overview'],
                          movie['original_language'],
                          movie['poster_path'],
                          movie['backdrop_path'],
                          ','.join(map(str, movie['genre_ids'])),
                          movie['vote_count'],
                          movie['vote_average'],
                          movie['popularity']])
                db.commit()
                print('Added movie', movie['title'], movie['release_date'], 'to database.')
        else:
            print('Got Response:', res.status_code, res.reason)


if __name__ == '__main__':
    #update_movie_db()
    #insert_test_users()
    #insert_test_polls()
    #db_file = "C:\\Dev\\repo\\CITS3403-Project1-SocialChoice\\data.db"
    #db = sqlite3.connect(db_file, check_same_thread=False)
    #db.execute('drop table poll_votes;')
    insert_test_poll_votes()
    pass
