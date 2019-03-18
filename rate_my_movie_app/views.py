from django.shortcuts import render
from django.http import HttpResponse

from rate_my_movie_app.models import Genre, UserProfile
from rate_my_movie_app.forms import UserForm, UserProfileForm

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


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile.picture']
            profile.save()

            registered = True
        
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rate_my_movie_app/register.html',
                  {'user_form': user_form,
                      'profile_form': profile_form,
                   'registered': registered})
