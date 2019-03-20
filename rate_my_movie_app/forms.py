from django import forms
from rate_my_movie_app.models import Movie, Genre
from registration.forms import RegistrationForm

class UserProfileRegistrationForm(RegistrationForm):
    pass



class MovieForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(MovieForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(MovieForm, self).save(commit=False)
        inst.uploader_id = self._user

        if commit:
            inst.save()
        return inst


    title = forms.CharField(max_length=64,
            help_text="Enter the title.")

    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all())

    description = forms.CharField(help_text="Enter a brief description.")
    
    release_date = forms.DateField(help_text="Enter the release date.")

    views = forms.IntegerField(
              widget=forms.HiddenInput(), 
              initial=0)
    total_rating = forms.IntegerField(
              widget=forms.HiddenInput(), 
              initial=0)
    number_ratings = forms.IntegerField(
              widget=forms.HiddenInput(), 
              initial=0)
    
    slug = forms.CharField(
                    widget=forms.HiddenInput(), 
                    required=False)

    class Meta:
        model = Movie
        exclude = ('uploader_id',)
		
		
class GenreForm(forms.ModelForm):
	genre = forms.CharField(max_length=64, help_text="Please enter the genre to be added.")
	
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)
	
	class Meta:
		model = Genre
		fields = ('genre',)
	
	
	
	
