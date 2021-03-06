from django.conf.urls import url
from rate_my_movie_app import views

#Maps out the urls for the websites so that links redirect correctly
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

        url('^create_modal_comment/(?P<author_id>[\w\-]+)-(?P<parent_id>[\w\-]+)-(?P<movie_id>[\w\-]+)/$', 
            views.CreateCommentModal.as_view(), 
            name='create_modal_comment'),
]
