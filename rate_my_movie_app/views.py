from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views import generic

from rate_my_movie_app.models import Genre, Movie, Comment, UserProfile
from rate_my_movie_app.forms import MovieForm, CommentForm, ModalCommentForm, GenreForm
from bootstrap_modal_forms.mixins import PassRequestMixin, DeleteAjaxMixin
from django.db.models import F


def home(request):
    """
    Handles the display of the home page which contains the top 5 most viewed pages 
    """
    
    movie_list = Movie.objects.order_by('-views')[:5]
    context_dict = {'movies': movie_list}
    
    return render(request, 'rate_my_movie_app/home.html', context_dict)


def aboutus(request):
    """
        ABOUT US
    """

    return render(request, 'rate_my_movie_app/aboutus.html')
	
def mostpopular(request):
	"""
          Handles the webpage the display of most viewed pages
        """
	movie_list = Movie.objects.order_by('-views').all()
	context_dict = {'movies': movie_list}
	
	return render(request, 'rate_my_movie_app/mostpopular.html', context_dict)

"""
   RUMOURS
"""
def rumours(request):
	return render(request, 'rate_my_movie_app/rumours.html')

def genres(request):
    """
	Handles display of the genres
    """
    genre_list = Genre.objects.all()
    context_dict = {'genres': genre_list}

    return render(request, 'rate_my_movie_app/genres.html', context_dict)


@login_required
def add_movie(request):
    """
            ADD MOVIE

            Handles user creation of new movies

    """
    # get the user profile of the user making the request
    user = UserProfile.objects.filter(user=request.user)[0]
	
    form = MovieForm(user=user)

    if request.method == "POST":
        form = MovieForm(request.POST, user=user)
		
    # Check the movie does not already exist in the database
        try:
            Movie.objects.get(title=request.POST.get('title', 'NULL'))
            form.add_error(None, "Movie with this title already exists.")
			
        except Movie.DoesNotExist:
            pass
			
        if form.is_valid():
            movie = form.save()
			
            # Add the movie thumbnail 
            if 'thumbnail' in request.FILES:
                movie.thumbnail = request.FILES['thumbnail']
			
            # Adds all of the chosen genres for the movie to its record
            for g in form.cleaned_data['genres']:
                movie.genres.add(g)
            movie.save()
			
            #Redirect the user to the most popular page where their movie will now be present
            return mostpopular(request)
        else:
            print(form.errors)
    return render(
            request, 
            'rate_my_movie_app/add_movie.html',
            {'form': form})


@login_required
def add_genre(request):
    """
        ADD GENRE

        Handles the user creation of new genres
    """
    form = GenreForm()
	
    if request.method == 'POST':
        form = GenreForm(request.POST)
		
        #  Ensures the genre does not already exist
        try:
            Genre.objects.get(genre=request.POST.get('genre', 'NULL'))
            form.add_error(None, "This genre already exists.")

        except Genre.DoesNotExist:
            pass # avoids having to indent everything below
			
		
        if form.is_valid():
            genre = form.save(commit = True)
			
            # Adds the chosen thumbnail
            if 'thumbnail' in request.FILES:
                genre.thumbnail = request.FILES['thumbnail']
                genre.save()
            return genres(request)
        else:
            print(form.errors)
    return render(request, 'rate_my_movie_app/add_genre.html', {'form': form})



def show_genre(request, genre_name_slug):
    """
        SHOW GENRE

        view function renders the selected genre to the user
    """
    context_dict = {}

    # Attempt to get the movies to be displayed on the page
    try:
        genre = Genre.objects.get(slug=genre_name_slug)

        movies = genre.movie_set.all()

        context_dict['movies'] = movies
        context_dict['genre'] = genre
	
    # display a no movies present message
    except Genre.DoesNotExist:	
        context_dict['genre'] = None
        context_dict['movies'] = None
    
    return render(
            request,
            'rate_my_movie_app/genre.html',
            context_dict)


def sort_comments(comments):
    """
  HELPER METHOD

  Orders (example below) so that they can be iterated and output in the template

  For a comment tree:

  - ROOT 1 
  -- CHILD 1
  --- GRANDCHILD 1
  -- CHILD 2
  - ROOT 2
  -ROOT 3

  Method will return [ROOT1, CHILD1, GRANDCHILD 1, CHILD 2, ROOT 2, ROOT 3]

    """
    def by_time(comment):
        return comment.time_stamp

    def is_root(comment):
        return comment.parent == None

    def children_of(comment):
        """
          recursive function 
          gathers the children and children of children ... etc. of comment passed as param, returns them in the ordering specified above 
        """
        ret = []
        for child in sorted(children[comment], key=by_time):
            ret.append(child)
            ret.extend(children_of(child))
        return ret


    # create a dictionary of {parent : [list of its children]}
    children = {comment:[child for child in comments 
                        if child.parent==comment] 
                for comment in comments}

    # get the root comments and order by time_stamp
    roots = sorted([comment for comment in comments if is_root(comment)], key=by_time)

    sorted_comments = []
    for root in roots:
        sorted_comments.append(root)
        sorted_comments.extend(children_of(root))

    return sorted_comments




def show_movie(request, movie_slug):
    """
       SHOW MOVIE

       Method for displaying a particular movie page to the user
    """
    context_dict = {}
    
	#  Attempt to retrieve the data to be displayed on the movies page
    try:
        movie = Movie.objects.get(slug=movie_slug)
        comments = Comment.objects.filter(movie=movie)

        context_dict['movie'] = movie

        context_dict['comments'] = sort_comments(comments)
        movie.views = movie.views + 1
        movie.save()

		#  If the user is logged in allow them to comment and reply to comments
        if  request.user.is_authenticated:
            author = UserProfile.objects.filter(
                    user=request.user)[0]

            form = CommentForm(
                    author=author,
                    parent=None,
                    movie=movie)

            context_dict['form'] = form

        else:
            context_dict['form'] = None

	#  if the user posts the comment form
        if request.method == "POST":
            form = CommentForm(
                    request.POST,
                    author=author,
                    parent=None,
                    movie=movie)
			
            if form.is_valid():
                comment = form.save(commit=False)
                comment.save()
                request.method="GET"
                return show_movie(request, movie_slug)

            else:
                print(form.errors)
    
    except Movie.DoesNotExist:
        context_dict['movie'] = None
        context_dict['comments'] = None
        context_dict['form'] = None

    return render(request, 
                  'rate_my_movie_app/movie.html',
                  context_dict)



class CreateCommentModal(PassRequestMixin, generic.CreateView):
    """
        CREATE REPLY MODAL

        Class based view for the creation of replies to comments on         a movie page
    """
    template_name = 'rate_my_movie_app/create_comment_modal.html'
    form_class = ModalCommentForm

   
    def get_form_kwargs(self):
        """
          pass arguments to the form from the url
        """
        kwargs = super(CreateCommentModal, self).get_form_kwargs()
        kwargs.update({
            "author":self.kwargs['author_id'],
            "parent":self.kwargs['parent_id'],
            "movie":self.kwargs['movie_id']})

        return kwargs

    def get_success_url(self):
        """
            return the user to movie page containing 
            the comment they were replying to
        """
        movie = Movie.objects.get(pk=self.kwargs['movie_id'])
        return "/rate_my_movie_app/movie/" + movie.slug + "/"

