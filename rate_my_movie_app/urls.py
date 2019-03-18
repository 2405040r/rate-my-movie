from django.conf.urls import url
from rate_my_movie_app import views


urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^aboutus/', views.aboutus, name='aboutus'),
	url(r'^mostpopular/', views.mostpopular, name='mostpopular'),
	url(r'^rumours/', views.rumours, name='rumours'),
	url(r'^genres/', views.genres, name='genres'),
]