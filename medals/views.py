from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import MedalsForm
from .models import Medals
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'medals/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'medals/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('addedmedals')
            except IntegrityError:
                return render(request, 'medals/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'medals/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'medals/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'medals/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('addedmedals')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createmedal(request):
    if request.method == 'GET':
        return render(request, 'medals/createmedal.html', {'form':MedalsForm()})
    else:
        try:
            form = MedalsForm(request.POST)
            newmedal = form.save(commit=False)
            newmedal.user = request.user
            newmedal.save()
            return redirect('addedmedals')
        except ValueError:
            return render(request, 'medals/createmedal.html', {'form':MedalsForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def currentmedals(request):
    medals = Medals.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'medals/addedmedals.html', {'medals':medals})

@login_required
def add_to_favorites(request):
    medals = Medals.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'medals/favouritesmedals.html', {'medals':medals})

@login_required
def viewmedal(request, medals_pk):
    medals = get_object_or_404(Todo, pk=medals_pk, user=request.user)
    if request.method == 'GET':
        form = MedalsForm(instance=todo)
        return render(request, 'medals/viewmedals.html', {'medals':medals, 'form':form})
    else:
        try:
            form = MedalsForm(request.POST, instance=medals)
            form.save()
            return redirect('addedmedals')
        except ValueError:
            return render(request, 'medals/viewmedals.html', {'medals':medals, 'form':form, 'error':'Bad info'})

@login_required
def deletemedals(request, medals_pk):
    medals = get_object_or_404(Medals, pk=medals_pk, user=request.user)
    if request.method == 'POST':
        medals.datecompleted = timezone.now()
        medals.save()
        return redirect('addedmedals')





"""@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')"""
