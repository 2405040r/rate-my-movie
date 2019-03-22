from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views import generic

from collections import defaultdict

from rate_my_movie_app.models import Genre, Movie, Comment, UserProfile
from rate_my_movie_app.forms import MovieForm, CommentForm, ModalCommentForm, GenreForm
from bootstrap_modal_forms.mixins import PassRequestMixin, DeleteAjaxMixin
from django.db.models import F

#When the page is requested by the user the corresponding function is called

def home(request):
	movie_list = Movie.objects.order_by('-views')[:5]
	context_dict = {'movies': movie_list}
	#The return statement refers to a html document locates in templates
	return render(request, 'rate_my_movie_app/home.html', context_dict)

def aboutus(request):
	return render(request, 'rate_my_movie_app/aboutus.html')
	
def mostpopular(request):
	movie_list = Movie.objects.order_by('-views').all()
	context_dict = {'movies': movie_list}
	
	return render(request, 'rate_my_movie_app/mostpopular.html', context_dict)

def rumours(request):
	return render(request, 'rate_my_movie_app/rumours.html')

def genres(request):
	genre_list = Genre.objects.all()
	context_dict = {'genres': genre_list}

	return render(request, 'rate_my_movie_app/genres.html', context_dict)

@login_required
def add_movie(request):
    user = UserProfile.objects.filter(user=request.user)[0]

    form = MovieForm(user=user)

    if request.method == "POST":
        form = MovieForm(request.POST, user=user)

        if form.is_valid():
            movie = form.save()

            if 'thumbnail' in request.FILES:
                movie.thumbnail = request.FILES['thumbnail']

            for g in form.cleaned_data['genres']:
                movie.genres.add(g)
                
            movie.save()
            

            return home(request)
        else:
            print(form.errors)
    
    return render(
            request, 
            'rate_my_movie_app/add_movie.html',
            {'form': form})

@login_required
def add_genre(request):
	form = GenreForm()
	
	if request.method == 'POST':
		form = GenreForm(request.POST)
		
		if form.is_valid():
			form.save(commit = True)
			
			return genres(request)
		else:
			print(form.errors)
	return render(request, 'rate_my_movie_app/add_genre.html', {'form': form})


def show_genre(request, genre_name_slug):
    context_dict = {}

    try:
        genre = Genre.objects.get(slug=genre_name_slug)

        movies = genre.movie_set.all()

        context_dict['movies'] = movies
        context_dict['genre'] = genre
		
    except Genre.DoesNotExist:	
        context_dict['genre'] = None
        context_dict['movies'] = None
    
    return render(
            request,
            'rate_my_movie_app/genre.html',
            context_dict)

def sort_comments(comments):
    def by_time(comment):
        return comment.time_stamp

    def is_root(comment):
        return comment.parent == None

    def children_of(comment):
        ret = []
        for child in sorted(children[comment], key=by_time):
            ret.append(child)
            ret.extend(children_of(child))
        return ret

    children = {comment:[child for child in comments 
                        if child.parent==comment] 
                for comment in comments}

    roots = sorted([comment for comment in comments if is_root(comment)], key=by_time)

    sorted_comments = []
    for root in roots:
        sorted_comments.append(root)
        sorted_comments.extend(children_of(root))

    return sorted_comments


def show_movie(request, movie_slug):
    context_dict = {}
    
    try:
        movie = Movie.objects.get(slug=movie_slug)
        comments = Comment.objects.filter(movie=movie)

        context_dict['movie'] = movie

        context_dict['comments'] = sort_comments(comments)
        movie.views = movie.views + 1
        movie.save()

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
    template_name = 'rate_my_movie_app/create_comment_modal.html'
    form_class = ModalCommentForm

    def get_form_kwargs(self):
        kwargs = super(CreateCommentModal, self).get_form_kwargs()
        kwargs.update({
            "author":self.kwargs['author_id'],
            "parent":self.kwargs['parent_id'],
            "movie":self.kwargs['movie_id']})

        return kwargs

    def get_success_url(self):
        movie = Movie.objects.get(pk=self.kwargs['movie_id'])
        return "/rate_my_movie_app/movie/" + movie.slug + "/"


