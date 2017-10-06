import datetime
import hashlib

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .blockchain import Block, reg

reg_block = Block(block='REG', timestamp=datetime.datetime.utcnow(), previous_hash=None)
vot_block = Block(block='VOT', timestamp=datetime.datetime.utcnow(), previous_hash=None)


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
    team_id = request.user.id
    voted = False
    registered_hash = reg_block.team_registered(team_id)
    if registered_hash:
        voted = vot_block.team_voted(registered_hash)
    users = list(User.objects.values('id', 'first_name'))
    registered_votizens = reg.find_one().get('transactions')
    votizens = []
    for u in users:
        merge = {}
        for r in registered_votizens:
            if u['id'] == r['team_id']:
                merge.update(u)
                merge.update(r)
                votizens.append(merge)
    return render(request, 'voting.html', {
        'votizens': sorted(votizens),
        'has_voted': voted
    })


@login_required
def vote(request, recipient=None):
    if recipient:
        team_id = request.user.id

        registered_hash = reg_block.team_registered(team_id)
        if registered_hash:
            voted = vot_block.team_voted(registered_hash)
            if not voted:
                vote_payload = {
                    'team_hash': registered_hash,
                    'recipient': recipient
                }
                vot_block.add_vot_transaction(vote_payload)

    return redirect('voting')


@login_required
def results(request):
    return render(request, 'results.html', {})
