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
             U("Quentin", "pass", "Password1234"),
             U("Chris Dickens", "Password12345", ""),
             U("Nick Cassavetes", "Password12345", ""),
			 U("Steven Speilberg", "Passwordisthis1", ""),
			 U("John Carpenter", "Passwordisthisit1", ""),
			 U("Batman Fan12", "Passwordisthisi1", "")
            ]

    users = [_add_user(u) for u in users]

    G = namedtuple('G', ['name', 'thumbnail'])
    genres = [
              G("action", "genre_thumbs/action.jpg"),
              G("crime", "genre_thumbs/crime.jpg"),
              G("comedy", "genre_thumbs/comedy.jpg"),
              G("drama", "genre_thumbs/drama.jpg"),
			  G("horror", "genre_thumbs/horror.jpg"),
			  G("romance", "genre_thumbs/romance.jpg"),
			  G("science fiction", "genre_thumbs/scifi.jpg"),
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
        'release_date',
        'thumbnail'])
    movies = [
              M(
                'Pulp Fiction',
                users[0],
                121310,
                12300,
                1275,
                "An American crime film.",
                [genres[0], genres[1]],
                datetime(1994,5,12),
                'movie_thumbs/pulp-fiction.jpg'),
              M(
                'Hot Fuzz',
                users[1],
                72331,
                9814,
                998,
                "A British buddy cop film starring Simon Peg",
                [genres[0], genres[1], genres[2]],
                date(2007,2,16),
                'movie_thumbs/hot-fuzz.jpg'),
              M(
                'The Notebook',
                users[2],
                52331,
                9800,
                998,
                "A poor man and rich woman who are in love struggle to make things work as their social differences separate them",
                [genres[3], genres[5]],
                date(2004,6,25),
                'movie_thumbs/the-notebook.jpg'),
              M(
                'E.T. the Extra-Terrestrial',
                users[2],
                100321,
                9530,
                988,
                "A child tries to help a friendly alien to escape earth to help it return home",
                [genres[6]],
                date(1982,12,10),
                'movie_thumbs/ET.jpg'),
              M(
                'Jaws',
                users[2],
                131321,
                9430,
                968,
                "A killer shark causes chaos at a beach resort",
                [genres[0], genres[3]],
                date(1975,12,26),
                'movie_thumbs/jaws.jpg'),
              M(
                'Halloween',
                users[3],
                91321,
                9630,
                1068,
                "15 years after murdering his sister Michael Myers is released from a mental hospital and returns home to kill again",
                [genres[4]],
                date(1978,1,25),
                'movie_thumbs/halloween.jpg'),
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
                         "Sooo good!!",
                         datetime(2019,3,2,12,0,3)),
                     C(
                         users[0],
                         movies[1],
                         None,
                         "This movie was actually so bad :(",
                         datetime(2019,3,2,12,1,0)),
                     C(
                         users[1],
                         movies[0],
                         None,
                         "A little violent",
                         datetime(2019,3,1,12,0,1)),
                     C(
                         users[1],
                         movies[2],
                         None,
                         "One of my favourite movies!",
                         datetime(2019,2,3,12,0,3)),
                     C(
                         users[4],
                         movies[2],
                         None,
                         "Normally i like scary stuff but this is a really great movie!",
                         datetime(2019,2,4,7,0,7)),
                     C(
                         users[4],
                         movies[3],
                         None,
                         "Not scary enough!",
                         datetime(2019,1,25,9,0,4)),
                     C(
                         users[0],
                         movies[3],
                         None,
                         "Can't believe it took me this long to watch this",
                         datetime(2018,7,2,9,0,1)),
                     C(
                         users[1],
                         movies[3],
                         None,
                         "The special effects were rubbish and ruined the immersion for me so i can't reccomend this",
                         datetime(2019,1,4,3,0,5)),
                     C(
                         users[3],
                         movies[4],
                         None,
                         "Hope you all enjoyed my movie!",
                         datetime(2018,9,10,1,0,1)),
                     C(
                         users[5],
                         movies[5],
                         None,
                         "This movie isn't even half as good as the Dark Night!",
                         datetime(2019,5,4,5,0,9)),


                    ]

    root_comments = [_add_comment(c) for c in root_comments]

    child_comments = [
                      C(
                          users[1],
                          movies[0],
                          root_comments[0],
                          "Biased much...",
                          datetime(2019,3,3,6,5,1)),
                      C(
                          users[0],
                          movies[5],
                          root_comments[0],
                          "Don't listen to him I think its awesome!",
                          datetime(2019,3,3,6,5,1)),
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
    g = Genre.objects.get_or_create(
            genre=gtuple.name,
            thumbnail=gtuple.thumbnail)[0]
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
            release_date=mtuple.release_date)[0]

    m.thumbnail=mtuple.thumbnail
    m.save()
    
    for genre in mtuple.genres:
        m.genres.add(genre)
    
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
