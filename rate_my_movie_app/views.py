from django.shortcuts import render
from django.http import HttpResponse

from rate_my_movie_app.models import Genre, UserProfile

#When the page is requested by the user the corresponding function is called

def home(request):
	#The return statement refers to a html document locates in templates
	return render(request, 'rate_my_movie_app/home.html')

def aboutus(request):
	return render(request, 'rate_my_movie_app/aboutus.html')
	
def mostpopular(request):
	return render(request, 'rate_my_movie_app/mostpopular.html')

def rumours(request):
	return render(request, 'rate_my_movie_app/rumours.html')

def genres(request):
	genre_list = Genre.objects.all() #.order_by('-likes')[:5]
	context_dict = {'genres': genre_list}

	return render(request, 'rate_my_movie_app/genres.html', context_dict)

