from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

short_char_field = 64

class UserProfile(models.Model):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE)

    profile_picture = models.ImageField(
            upload_to='profile_pics',
            blank=True)

    def __str__(self):
        return self.user.username
		
class Genre(models.Model):
	genre = models.CharField(max_length=short_char_field)
	slug = models.SlugField()
	
	thumbnail = models.ImageField(upload_to='genre_thumbs', blank=True)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.genre)
		super(Genre,self).save(*args, **kwargs)
	
	def __str__(self):
		return f"{self.genre}"

class Movie(models.Model):
    title = models.CharField(max_length=short_char_field)
    genres = models.ManyToManyField(Genre, blank=True)
    uploader_id = models.ForeignKey(UserProfile, 
            on_delete=models.PROTECT)
    description = models.TextField()
    release_date = models.DateField()
    
    views = models.IntegerField(default=0)
    total_rating = models.IntegerField(default=0)
    number_ratings = models.IntegerField(default=0)

    slug = models.SlugField()

    thumbnail = models.ImageField(
            upload_to='movie_thumbs', 
            blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.title}-{self.release_date.year}")
        super(Movie,self).save(*args, **kwargs)
    
    def get_average_rating(self):
        return self.total_rating / self.number_ratings if self.number_ratings != 0 else 0

    def get_genres(self):
        return ', '.join([g.genre for g in self.genres.all()])

    def __str__(self):
        return f"{self.title} ({self.release_date})"

class Comment(models.Model):
    author = models.ForeignKey(UserProfile, 
            on_delete=models.PROTECT)
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
    parent = models.ForeignKey('self', null=True, on_delete=models.PROTECT) 
    time_stamp = models.DateTimeField()
    body = models.TextField()

    def get_indent_level(self):
        indent = 0
        comment = self
        while comment.parent != None:
            indent += 1
            comment = comment.parent
        
        return indent


    def as_padding(self):
        return 20 * self.get_indent_level()

    def __str__(self):
        return f"{self.author}@{self.time_stamp}: {self.body}"

