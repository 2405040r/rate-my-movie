from django.contrib import admin

from rate_my_movie_app.models import Genre, Movie, UserProfile, Comment
# Register your models here.


admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(UserProfile)
admin.site.register(Comment)
