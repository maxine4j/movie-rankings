import requests
import sqlite3
import time
import os


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
    update_movie_db()
