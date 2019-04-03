from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def register_view(request,*args,**kwargs):
	print(	request.GET.get('username'))
	if (request.method == 'POST'):
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
			print(username)
			return redirect('index')
	else:
		form = UserRegisterForm()
	return render(request, 'web/register.html', {'form': form})