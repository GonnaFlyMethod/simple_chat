from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.views import View
from django.shortcuts import render, redirect

from .forms import SignInForm



class SignUpView(View):

	def get(self, request):
		context = {}
		context['sign_up_form'] = UserCreationForm()

		return render(request, 'accounts/sign_up.html', context)


	def post(self, request):
		sign_up_form = UserCreationForm(request.POST)

		if sign_up_form.is_valid():
			sign_up_form.save()

			return redirect('accounts:sign-in')

		context = {'sign_up_form': sign_up_form}
		return render(request, 'accounts/sign_up.html', context)



class SignInView(View):

	def get(self, request):
		context = {}
		context['sign_in_form'] = SignInForm()

		return render(request, 'accounts/sign_in.html', context)


	def post(self, request):
		sign_in_form = SignInForm(request.POST)

		if sign_in_form.is_valid():
			user = sign_in_form.login(request)
			if user:
				login(request, user)
				return redirect('chat:thread-list')
    	
		context = {'sign_in_form': sign_in_form}
		return render(request, 'accounts/sign_in.html', context)


def logout_view(request):
    logout(request)
    return redirect('accounts:sign-in')