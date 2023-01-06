from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import unauthenticated_user

from django.contrib.auth import login, logout, authenticate

from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
#===============================================================

from accounts.models import CustomUser


# Register a new User
def register_user(request):
	template = 'accounts/register.html'

	if request.method == "POST":
		username = request.POST.get("username")
		email = request.POST.get("email")
		password = request.POST.get("password")
		confirm_password = request.POST.get("confirm_password")

		if CustomUser.objects.filter(email=email).exists():
			messages.info(request, "An account with that email already exists")
			return redirect("accounts:register")

		user = CustomUser.objects.create_user(username=username, email=email, password=password)
		user.set_password(password)
		messages.success(request, f'Account created for {username.title()}')
		print(f"Success!!! Account Created for {username}")
		user.save()
		# login(request, user)
		return redirect("accounts:home")

	return render(request, template)

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)

		if password_reset_form.is_valid():
			email = password_reset_form.cleaned_data['email']
			associated_users = CustomUser.objects.filter(Q(email=email))

			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"

					email_template = "accounts/password/password_reset_email.txt"

					extra = {
					"email":user.email,
					'domain':'127.0.0.1:8000',#!
					'site_name': 'TO DO',#!
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',#!
					}

					email = render_to_string(email_template, extra)
					
					try:
						send_mail(subject, email, 'simplenick01@gmail.com',[user.email,], fail_silently=False) #! change admin later
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ('accounts:password_reset_done')#!
	password_reset_form = PasswordResetForm()
  
	return render(request=request, template_name="accounts/password/password_reset.html", context={"password_reset_form":password_reset_form},)

@login_required(login_url="/qr-gen/accounts/login") #! Modify Login URL
def log_out(request):
	logout(request)
	messages.success(request, f"You Have been logged out")
	return redirect('qr_generator:home',) # pk=str(request.user.id)

@login_required(login_url="/qr-gen/accounts/login")
def dashboard(request):
	context = {}
	return redirect('qr_generator:home')

def home(request):
	return HttpResponse("Welcome Home!!!")
