import requests
import sqlite3
import os
import time
import random
import json
import psycopg2
#from movie_rankings.data import init_db


# config
db_file = 'data.db'
user_count = 5000
poll_count = 500
avg_poll_choice_count = 8
avg_poll_comment_count = 15
avg_poll_vote_count = 50
avg_user_fav_count = 30
movies_count = 10000


def load_names(path):
    with open(path, 'r') as f:
        names = json.load(f)
    return names


def load_lipsum(path):
    with open(path, 'r') as f:
        contents = f.read()
        words = contents.split(' ')
    return words

lipsum = load_lipsum('lipsum.txt')
names = load_names('names.json')


def generate_lipsum_text(word_count):
    text = ''
    for i in range(word_count):
        next_word = random.choice(lipsum)
        text = '{} {}'.format(text, next_word)
    return text


def build_users(sql):
    users = []
    for res in sql:
        users.append({
            'id': res[0],
            'name': res[1],
            'admin': res[2],
        })
    return users


def build_polls(sql):
    polls = []
    for res in sql:
        polls.append({
            'id': res[0],
            'creator_user_id': res[1],
            'title': res[2],
            'description': res[3],
        })
    return polls


def build_poll_votes(sql):
    poll_votes = []
    for res in sql:
        poll_votes.append({
            'id': res[0],
            'poll_id': res[1],
            'choice_id': res[2],
            'user_id': res[3],
        })
    return poll_votes


def build_poll_comments(sql):
    poll_comments = []
    for res in sql:
        poll_comments.append({
            'id': res[0],
            'poll_id': res[1],
            'user_id': res[2],
            'body': res[3],
            'timestamp': res[4],
        })
    return poll_comments


def build_poll_choices(sql):
    poll_choices = []
    for res in sql:
        poll_choices.append({
            'id': res[0],
            'poll_id': res[1],
            'movie_id': res[2],
        })
    return poll_choices


def build_movies(sql):
    movies = []
    for res in sql:
        movies.append({
            'id': res[0],
            'title': res[1],
            'release_date': res[2],
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


def build_favourites(sql):
    favourites = []
    for res in sql:
        favourites.append({
            'id': res[0],
            'user_id': res[1],
            'movie_id': res[2],
        })
    return favourites


def fetch_movies(db):
    url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc"
    api_key = os.environ.get('THEMOVIEDB_KEY')
    cur = db.cursor()
    for i in range(1, int(movies_count / 20)):
        req_url = url + '&api_key=' + api_key + '&page=' + str(i)
        print('Getting page =', i, 'URL =', req_url)
        res = requests.get(req_url)
        if res.ok:
            print('Got Response:', res.status_code, res.reason)
            res_json = res.json()
            for movie in res_json['results']:
                cur.execute('''
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
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
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
                try:
                    print('Added movie', movie['title'], movie['release_date'], 'to database.')
                except:
                    pass
        else:
            print('Got Response:', res.status_code, res.reason)
    db.commit()
    cur.close()


def generate_users(db):
    cur = db.cursor()
    for i in range(user_count):
        is_boy = random.choice([True, False])
        if is_boy:
            name = "{} {}".format(random.choice(names['boy']), random.choice(names['last']))
        else:
            name = "{} {}".format(random.choice(names['girl']), random.choice(names['last']))
        cur.execute('INSERT INTO users(id, name) VALUES (%s,%s);', [i, name])
        if i % 100 == 0: print('Generated User:', i, name)
    db.commit()
    cur.close()
    print('\tDONE GENERATING USERS')


def generate_polls(db):
    cur = db.cursor()
    cur.execute('SELECT * FROM users;')
    users = build_users(cur.fetchall())
    for i in range(poll_count):
        user_id = random.choice(users)['id']
        title = generate_lipsum_text(random.randrange(2, 6)).title()
        desc = generate_lipsum_text(random.randrange(3, 15)).title()
        cur.execute('''
            INSERT INTO polls(
                creator_user_id,
                title,
                description
            ) VALUES(%s, %s, %s);
        ''', [user_id, title, desc])
        if i % 100 == 0: print('Generated Poll:', i, title)
    db.commit()
    cur.close()
    print('\tDONE GENERATING POLLS')


def generate_poll_choices(db):
    cur = db.cursor()
    cur.execute('SELECT * FROM polls;')
    polls = build_polls(cur.fetchall())
    cur.execute('SELECT * FROM movies;')
    movies = build_movies(cur.fetchall())
    for i in range(avg_poll_choice_count * poll_count):
        poll_id = random.choice(polls)['id']
        movie_id = random.choice(movies)['id']
        cur.execute('''
            INSERT INTO poll_choices(
                poll_id,
                movie_id
            ) VALUES(%s, %s) ON CONFLICT DO NOTHING;
        ''', [poll_id, movie_id])
        if i % 100 == 0: print('Generated Poll Choice:', i, poll_id, movie_id)
    db.commit()
    cur.close()
    print('\tDONE GENERATING POLL CHOICES')


def generate_poll_comments(db):
    cur = db.cursor()
    cur.execute('SELECT * FROM polls;')
    polls = build_polls(cur.fetchall())
    cur.execute('SELECT * FROM users;')
    users = build_users(cur.fetchall())
    for i in range(avg_poll_comment_count * poll_count):
        poll_id = random.choice(polls)['id']
        user_id = random.choice(users)['id']
        body = generate_lipsum_text(random.randrange(2, 15))
        timestamp = time.time() - random.randrange(0, 60 * 60 * 24 * 5)
        cur.execute('''
            INSERT INTO poll_comments(
                poll_id,
                user_id,
                body,
                timestamp
            ) VALUES(%s, %s, %s, %s);
        ''', [poll_id, user_id, body, timestamp])
        if i % 100 == 0: print('Generated Poll Comment:', i, body)
    db.commit()
    cur.close()
    print('\tDONE GENERATING POLL COMMENTS')


def generate_poll_votes(db):
    cur = db.cursor()
    cur.execute('SELECT * FROM polls;')
    polls = build_polls(cur.fetchall())
    cur.execute('SELECT * FROM users;')
    users = build_users(cur.fetchall())
    for i in range(avg_poll_vote_count * poll_count):
        poll_id = random.choice(polls)['id']
        cur.execute('SELECT * FROM poll_choices WHERE poll_id = %s;', [poll_id])
        choices = build_poll_choices(cur.fetchall())
        if len(choices) < 1:
            print('current poll has no choices...')
            continue
        choice_id = random.choice(choices)['id']
        user_id = random.choice(users)['id']
        cur.execute('''
            INSERT INTO poll_votes(
                poll_id,
                choice_id,
                user_id
            ) VALUES(%s, %s, %s) ON CONFLICT DO NOTHING;
        ''', [poll_id, choice_id, user_id])
        if i % 100 == 0: print('Generated Poll Vote:', i, poll_id, choice_id, user_id)
    db.commit()
    cur.close()
    print('\tDONE GENERATING POLL VOTES')


def generate_favourites(db):
    cur = db.cursor()
    cur.execute('SELECT * FROM users;')
    users = build_users(cur.fetchall())
    cur.execute('SELECT * FROM movies;')
    movies = build_movies(cur.fetchall())
    for i in range(avg_user_fav_count * user_count):
        user_id = random.choice(users)['id']
        movie_id = random.choice(movies)['id']
        cur.execute('''
            INSERT INTO favourites(
                user_id,
                movie_id
            ) VALUES(%s, %s) ON CONFLICT DO NOTHING;
        ''', [user_id, movie_id])
        if i % 100 == 0: print('Generated Favourite:', i, user_id, movie_id)
    db.commit()
    cur.close()
    print('\tDONE GENERATING FAVOURITES')


def drop_all_but_movies(db):
    return False
    db.execute('DROP TABLE IF EXISTS favourites;')
    db.execute('DROP TABLE IF EXISTS poll_choices;')
    db.execute('DROP TABLE IF EXISTS poll_comments;')
    db.execute('DROP TABLE IF EXISTS poll_votes;')
    db.execute('DROP TABLE IF EXISTS polls;')
    db.execute('DROP TABLE IF EXISTS users;')


def main():
    #db = sqlite3.connect(db_file, check_same_thread=False)
    db = psycopg2.connect('dbname=tim user=tim')
    #drop_all_but_movies(db)
    #init_db(db_file)
    #fetch_movies(db) # This can take a while
    generate_users(db)
    generate_favourites(db)
    generate_polls(db)
    time.sleep(1)
    generate_poll_choices(db)
    time.sleep(1)
    generate_poll_votes(db)
    time.sleep(1)
    generate_poll_comments(db)
    time.sleep(1)

if __name__ == '__main__':
    main()
