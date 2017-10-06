import datetime
import hashlib

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .blockchain import Block


def home(request):
    if request.user.is_authenticated():
        return redirect('voting')
    return render(request, 'home.html', {})


def signup(request):
    if request.user.is_authenticated():
        return redirect('voting')
    if request.method == 'POST':
        team_name = request.POST['team_name']
        email = request.POST['email']
        password = request.POST['password']

        team = User(first_name=team_name, username=email)
        team.set_password(password)
        team.save()

        team_id = team.id
        team_hash = hashlib.sha256(team.password.encode()).hexdigest()
        team_payload = {
            'team_id': team_id,
            'team_hash': team_hash
        }
        reg_block = Block(
            block='REG', timestamp=datetime.datetime.utcnow(), previous_hash=None)
        reg_block.add_reg_transaction(team_payload)

        return render(request, 'login.html', {'success': True})

    return render(request, 'signup.html', {'title': 'Votizen - Sign Up'})


def user_login(request):
    ctx = {
        'errors': False
    }
    if request.user.is_authenticated():
        return redirect('voting')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('voting')
        ctx['errors'] = True
    return render(request, 'login.html', context=ctx)


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def voting(request):
    votizens = User.objects.all()
    return render(request, 'voting.html', {
        'votizens': votizens
    })
