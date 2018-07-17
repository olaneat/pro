from django.test import TestCase

from catalog.models import Author

class AuthorModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		Author.objects.create(first_name = 'Biggy', surname = 'Fatty')

    
	def first_name_max_lemgth(self):
		author = Author.objects.get(id = 1)
		max_length  = author._meta.get_field('first_name').max_length
		self.assertEquals(max_length, 100)

	def test_D_0_D_label(self):
		author=Author.objects.get(id=1)
		field_label = author._meta.get_field('D_O_D').verbose_name
		self.assertEquals(field_label,'died')
	
	def test_first_name_max_length(self):
		author=Author.objects.get(id=1)
		max_length = author._meta.get_field('first_name').max_length
		self.assertEquals(max_length,100)

	def object_name_is_surname_comma_first_name(self):
		author=Author.objects.get(id=1)
		expected_object_name = '%s, %s' % (author.surname, author.first_name)
		self.assertEquals(expected_object_name,str(author))

	def test_get_absolute_url(self):
		author = Author.objects.get(id = 1)
		self.assertEquals(author.get_absolute_url(), '/catalog/author/1')

	def test_surname_label(self):
		author = Author.objects.get(id = 1)
		field_label = author._meta.get_field('surname').verbose_name
		self.assertEquals(field_label, 'surname')

#	def test_D_O_B_label(self):
#		author = Author.objects.get(id = 1)
#		field_label = Author._meta.get_field('D_O_B').verbose_name
#		self.assertEquals(field_label, 'D_O_B')

	