from django.test import TestCase

from rate_my_movie_app.models import Genre, Comment
from django.conf import settings
import os

from rate_my_movie_app import views

class TemplateTest(TestCase):
	
	def test_base_template_exists(self):
        # Check base.html is in the correct folder template folder
		path_to_base = settings.TEMPLATE_DIR + '/rate_my_movie_app/base.html'
		self.assertTrue(os.path.isfile(path_to_base))
		
class StaticTest(TestCase):
	def test_logo_in_static_folder(self):
		#Check the logo is in the static media folder
		path_to_logo = settings.STATIC_DIR + '/images/site-logo.png'
		self.assertTrue(os.path.isfile(path_to_logo))
		
		
class GenreMethodTest(TestCase):
	def test_ensure_genre_is_added(self):
		#Ensures the new genre has been added
		g = Genre(genre= 'test')
		g.save()

		self.assertEqual(str(Genre.objects.get(genre=g)), 'test')
		
	