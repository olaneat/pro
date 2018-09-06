
def signUp(request):
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
			return redirect('index.html')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form':form})
