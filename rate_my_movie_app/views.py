from django.shortcuts import render
from django.http import HttpResponse

from rate_my_movie_app.models import Genre, Movie, Comment, UserProfile
from rate_my_movie_app.forms import MovieForm


#When the page is requested by the user the corresponding function is called

def home(request):
	#The return statement refers to a html document locates in templates
	return render(request, 'rate_my_movie_app/home.html')

def aboutus(request):
	return render(request, 'rate_my_movie_app/aboutus.html')
	
def mostpopular(request):
	movie_list = Movie.objects.all() #.order_by('-likes')[:5]
	context_dict = {'movies': movie_list}
	
	return render(request, 'rate_my_movie_app/mostpopular.html', context_dict)

def rumours(request):
	return render(request, 'rate_my_movie_app/rumours.html')

def genres(request):
	genre_list = Genre.objects.all() #.order_by('-likes')[:5]
	context_dict = {'genres': genre_list}

	return render(request, 'rate_my_movie_app/genres.html', context_dict)

def add_movie(request):
    user = UserProfile.objects.filter(user=request.user)[0]

    form = MovieForm(user=user)

    if request.method == "POST":
        form = MovieForm(request.POST, user=user)

        if form.is_valid():
            movie = form.save(commit=True)
            return home(request)
        else:
            print(form.errors)
    
    return render(
            request, 
            'rate_my_movie_app/add_movie.html',
            {'form': form})

def show_genre(request, genre_name_slug):
	#Create a context dictionary
	#Use to pass to the template rendering engine
	context_dict = {}
	
	try:
		genre = Genre.objects.get(slug=genre_name_slug)
		
		movies = Movie.objects.filter(genre=genre)
		
		context_dict['movies'] = movies
		
		context_dict['genre'] = genre
		
	except Genre.DoesNotExist:
		
		context_dict['genre'] = None
		context_dict['movies'] = None
		
	return render(request, 'rate_my_movie_app/genre.html', context_dict)
		