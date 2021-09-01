from django.shortcuts import render, redirect
from .forms import LoginForm
from .models import BoardMember
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.

def register(request):
		if request.method == 'GET':
			return render(request, 'register.html')
		elif request.method == 'POST':
			username = request.POST.get('username', None)
			email = request.POST.get('email', None)
			password = request.POST.get('password', None)
			re_password = request.POST.get('re_password', None)
			res_data = {}
			if not (username and email and password and re_password):
				res_data['error'] = '모든 값을 입력해야 합니다'

			if password != re_password:
				res_data['error'] = '비밀번호가 다릅니다.'

			else:
				member = BoardMember(
					username=username,
					password=make_password(password),
					email=email,
				)
				member.save()

				return render(request, 'register.html', res_data)

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def Home(request):
    return render(request, 'home.html')

def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')