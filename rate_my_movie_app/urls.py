from django.conf.urls import url
from rate_my_movie_app import views


urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^aboutus/', views.aboutus, name='aboutus'),
	url(r'^mostpopular/', views.mostpopular, name='mostpopular'),
	url(r'^rumours/', views.rumours, name='rumours'),	
	url(r'^genres/', views.genres, name='genres'),
	
	url(r'^add_genre/$', views.add_genre, name='add_genre'),
	url(r'^genre/(?P<genre_name_slug>[\w\-]+)/$',
		views.show_genre, name='show_genre'),

        url(r'movie/(?P<movie_slug>[\w\-]+)/$', 
            views.show_movie, name='show_movie'),
	
        url(r'^add_movie/$', views.add_movie, name='add_movie'),
]
