from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import SignUpForm
import datetime
from django.contrib.auth import login, authenticate
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic
from .models import Book, Author, Language, BookInstance, Genre
from .forms import RenewBookForm
from django.contrib.auth.forms  import UserCreationForm


# Create your views here.


class AuthorCreate(CreateView):
	model  = Author
	fields  = '__all__'
	initial  = {'date_of_death': '15/05/1998',}

class AuthorUpdate(UpdateView):
	model  = Author
	fields  =['firstname', 'surname', 'D_O_B', 'D_O_D']

class AuthorDelete(DeleteView):
	model = Author
	successful_url = reverse_lazy('authors')	
def index(request):
	num_books=Book.objects.all().count()
	num_instances=BookInstance.objects.all().count()
	num_instances_available=BookInstance.objects.filter(status__exact='A').count()
	num_authors=Author.objects.count()
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits+1


	return render(
        request,
        'index.html',
  		context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors, 'num_visits': num_visits},
    )

class BookListView(generic.ListView):
	model = Book
	paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    """
    Generic class-based list view for a list of authors.
    """
    model = Author
    paginate_by = 10 


class AuthorDetailView(generic.DetailView):
    """
    Generic class-based detail view for an author.
    """
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='O').order_by('due_back')

class LoanedBooksDisplayListView(PermissionRequiredMixin, generic.ListView):
	model = BookInstance
	permission_required = 'catalog.can_mark_returned'
	template_name = 'catalog/bookinstance_list_display.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(status__exact = 'O').order_by('due_back')
		

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(self):
	book_inst = get_onbject_or_404(BookInstance, pk = pk)

	if request.methode == 'POST':
		form = RenewBookForm(request.POST)

		if form.is_valid():
			book_inst.due_back =form.cleaned_data['renewal_date']
			book_inst.save()

			return HttpResponseRedirect(reverse('index'))
	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks = 3 )
		form = RenewBookForm(initial = {'renewal_date': proposed_renewal_date,})

	return render(request, 'catalog/book_renew_librarian.html', {'forms':form, 'book_inst':book_inst})


def get(self, request):
	form = self.form_class(None)
	return render(request, self.template_name, {'form': form})

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit = False)
			user.refresh_from_db()
			user.profile.birth_date = form.cleaned_data.get('birth_date')
			user.save() 
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			subject = 'Activate Your Library account'
			message = render_to_string ('account_activation_email.html',{
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token(user)
				})
			user.email_user(subject, message)
			return redirect('account_activation_sent')
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user =authenticate(username = username, password = raw_password)
			login(request, user)
			return redirect('index')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form':form})

