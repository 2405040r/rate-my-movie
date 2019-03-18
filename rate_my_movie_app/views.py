from django.shortcuts import render
from django.http import HttpResponse

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
