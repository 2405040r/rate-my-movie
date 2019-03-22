from django.contrib import admin
from rate_my_movie_app.models import Genre, Movie, Comment, UserProfile


#Add these to the django admin page
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(UserProfile)
