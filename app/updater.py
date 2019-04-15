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
    pass
