import os
from collections import namedtuple
from datetime import date, datetime

os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'rate_my_movie.settings')

import django
django.setup()

from django.contrib.auth.models import User

from rate_my_movie_app.models import UserProfile, Genre, Movie, Comment

def populate():
    U = namedtuple('U', ['name', 'password', 'picture'])
    users = [
             U("Quentin", "pass", ""),
             U("Chris Dickens", "word", "")
            ]

    users = [_add_user(u) for u in users]

    G = namedtuple('G', ['name'])
    genres = [
              G("action"),
              G("crime"),
              G("comedy"),
              G("drama")
             ]
    
    genres = [_add_genre(g) for g in genres] 
    
    M = namedtuple('M', [
        'title', 
        'uploader',
        'views', 
        'total_rating',
        'number_ratings',
        'description',
        'genres',
        'release_date'])
    movies = [
              M(
                'Pulp Fiction',
                users[0],
                121310,
                12300,
                1130,
                "An American crime film.",
                [genres[0], genres[1]],
                datetime(1994,5,12)),
              M(
                'Hot Fuzz',
                users[1],
                72331,
                9814,
                998,
                "A British buddy cop film starring Simon Peg",
                [genres[0], genres[1], genres[2]],
                date(2007,2,16))
             ]

    movies = [_add_movie(m) for m in movies]

    C = namedtuple('C',[
        'user',
        'movie',
        'parent',
        'body',
        'time_stamp'])

    root_comments = [
                     C(
                         users[0],
                         movies[0],
                         None,
                         "Sooo good!! *****",
                         datetime(2019,3,2,12,0,3)),
                     C(
                         users[0],
                         movies[1],
                         None,
                         "Bad :(",
                         datetime(2019,3,2,12,1,0)),
                     C(
                         users[1],
                         movies[0],
                         None,
                         "A little violent ***",
                         datetime(2019,3,1,12,0,1))
                    ]

    root_comments = [_add_comment(c) for c in root_comments]

    child_comments = [
                      C(
                          users[1],
                          movies[0],
                          root_comments[0],
                          "Biased much...",
                          datetime(2019,3,3,6,5,1))
                     ]

    child_comments = [_add_comment(c) for c in child_comments]
        


def _add_user(utuple):
    u = User.objects.get_or_create(
            username=utuple.name,
            password=utuple.password)[0]
    
    u.save()

    up = UserProfile.objects.get_or_create(user=u)[0]

    up.save()

    return up

def _add_genre(gtuple):
    g = Genre.objects.get_or_create(genre=gtuple.name)[0]
    g.save()
    return g

def _add_movie(mtuple):
    m = Movie.objects.get_or_create(
            title=mtuple.title,
            uploader_id=mtuple.uploader,
            views=mtuple.views,
            total_rating=mtuple.total_rating,
            number_ratings=mtuple.number_ratings,
            description=mtuple.description,
            release_date=mtuple.release_date
            )[0]

    m.save()
    m.genres.add(*mtuple.genres)
    return m

def _add_comment(ctuple):
    c = Comment.objects.get_or_create(
            author=ctuple.user,
            movie=ctuple.movie,
            parent=ctuple.parent,
            body=ctuple.body,
            time_stamp=ctuple.time_stamp)[0]
    
    c.save()
    return c

if __name__=="__main__":
    print("Populating 'Rate My Movie' app database.")
    populate()
