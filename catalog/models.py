from django.contrib.auth.models import User
from datetime import date
from django.db import models
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
# Create your models here.

class Genre(models.Model):
	"A Model representing the Genre of the book"

	name = models.CharField(max_length = 200, help_text = 'Enter the book\'s Genre')

	def __str__(self):
		return self.name

class Book(models.Model):
	title = models.CharField(max_length = 200, help_text = "Enter the book's title here")
	author = models.ForeignKey('Author', on_delete = models.SET_NULL, null = True)
	genre = models.ManyToManyField(Genre, help_text = 'Enter the Genre for the book')
	summary = models.TextField(max_length = 1000, help_text = 'enter the book is brief summary')
	upload = models.FileField(upload_to = 'uploads', default =  True)
	isbn = models.CharField(max_length = 15, help_text = '13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
	#dialet = models.ForeignKey('Language', on_delete = models.SET_NULL, null = True)

	def __str__(self):
		"A string representing the Book Model"
		return self.title


	def get_absolute_url(self):
		"use to otain the detailed url for a particular book"

		return reverse ('book-detail', args = [str(self.id)])

	def display_genre(self):
		return ', '.join([ genre.name for genre in self.genre.all()[:3] ])

	display_genre.short_description = 'Genre'

class Author(models.Model):
	first_name = models.CharField(max_length = 100)
	surname = models.CharField(max_length = 200)
	D_O_B = models.DateField(null = True, blank = True)
	D_O_D = models.DateField('died', null = True, blank = True)

	class Meta:
		ordering = ["surname", "first_name"]

	def get_absolute_url(self):
		return reverse ('author-detail', args = [str(self.id)])
		
	def __str__(self):
		return '%s, %s'%(self.surname, self.first_name)
	
	
	def __str__(self):
		return '{0}, {1}'.format(self.surname, self.first_name)


class BookInstance(models.Model):
	"models representing the book copy"
	id = models.UUIDField(primary_key = True, default = uuid.uuid4, help_text = "unique id for the particular book")
	imprint = models.CharField(max_length = 200)
	book = models.ForeignKey('Book', on_delete = models.SET_NULL, null = True)
	borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	LOAN_STATUS = (
		('A', 'Available'),
		('O', 'On Loan'),
		('R', 'Reserved'),
		('M', 'Maintatnce'),
		)

	due_back = models.DateField(blank = True, null = True)
	status = models.CharField(max_length = 1, default = 'A', choices = LOAN_STATUS, help_text = 'Enter the books status')
	#librarian = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null =True)

	@property
	def is_overdue(self):
		if self.due_back and date.today() > self.due_back:
			return True
		return False

	class Meta:
		ordering = ['due_back']
		permissions = (("can_mark_return", "set book as returned"),
			)

	def __str__(self):
		return "{0}, ({1})".format(self.id, self.book.title)

class Language(models.Model):
	local_dialet = models.CharField(max_length  = 200, help_text = "enter the books Language")

	def __str__(self):
		return self.local_dialet


class profile(models.Model):
	user  = models.OneToOneField(User, on_delete = models.CASCADE)
	bio = models.TextField(max_length = 1000, blank = True)
	location = models.CharField(max_length = 30, blank = True)
	birth_date =  models.DateField(null = False)
	email_confirm =  models.BooleanField(default = False)
0


@receiver(post_save, sender = User)
def create_user_profile(sender,  instance, created, **kwargs):
	if created:
		profile.objects.create(user = instance)
	
#def update_user_profile(sender, instance, creted, **kwargs):
#	if created:
#		profile.objects.create(user = instance)


#@receiver(post_save, sender = User)
#def save_user_profiles(sender, profile, **kwargs):
#	instance.profile.save()


