from django.urls import path
from django.conf.urls import url
from .import views

urlpatterns = [
	path('', views.index, name='index'),
	path('books/', views.BookListView.as_view(), name='books'),
	path('book/<int:pk>', views.BookDetailView.as_view(), name = 'book-detail'),
	path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name = 'my-borrow'),
    path('mybooks/', views.LoanedBooksDisplayListView.as_view(), name = 'staff'),
    path('signup/', views.signup, name = 'signup' ),
    #url(r'^account_activation_sent/$', views.account_activation_sent, name = 'account_activation_sent'),
    #url(r'^activate/(?<uidb64>[0-9A-Za_\-+]/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
      #  views.activate, name='activate'),
]

urlpatterns += [   
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [  
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]

urlpatterns += [   
]

