from django.contrib import admin
from .models import Genre, Author, Book, BookInstance, Language


#admin.site.register(Book)
#admin.site.register(Author)
#admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)

@admin.register(Author)
class Authoradmin(admin.ModelAdmin):
	list_display = ('surname', 'first_name', 'D_O_B', 'D_O_D')
	fields = ['first_name', 'surname', ('D_O_B', 'D_O_D')]

@admin.register(BookInstance)
class BookInstanceadmin(admin.ModelAdmin):
	list_display = ('status', 'due_back', 'id', 'book', 'borrower',)
	list_filter = ('status', 'due_back',)

	fieldsets = (
		(None,{
			'fields': ('book', 'imprint', 'id')
			}),
		('Availability',{
			'fields': ('status', 'due_back', 'borrower',)
			})
		)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class Bookadmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'display_genre' )
	inlines = [BooksInstanceInline]

	

