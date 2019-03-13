from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from recipebox.models import Recipe, Author
from recipebox.forms import AddRecipe, AddAuthor, AddUser, Login


def mainpage(request):
    recipes = Recipe.objects.all()

    return render(request, 'mainpage.html', {'data': recipes})


def recipe(request, r_id):
    recipe = Recipe.objects.filter(id=r_id).first()

    return render(request, 'recipe.html', {'data': recipe})


def author(request, a_id):
    author = Author.objects.filter(id=a_id).first()
    recipes = Recipe.objects.filter(author=a_id)

    return render(request, 'author.html', {'a_data': author, 'r_data': recipes})


def addrecipe(request):
    form = None

    if request.method == 'POST':
        form = AddRecipe(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            Recipe.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                time_req=data['time_req'],
                instructions=data['instructions']
            )

            return render(request, 'success.html')

    else:
        form = AddRecipe()

    return render(request, 'generic_form.html', {'form': form})


def addauthor(request):
    form = None

    if request.method == 'POST':
        form = AddAuthor(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            Author.objects.create(
                name=data['name'],
                user=data['user'],
                bio=data['bio']
            )

            return render(request, 'success.html')

    else:
        form = AddAuthor()

    return render(request, 'generic_form.html', {'form': form})


def signup(request):
    form = None

    if request.method == 'POST':
        form = AddUser(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['username'],
                data['email'],
                data['password']
            )

            login(request, user)

            Author.objects.create(
                name=data['name'],
                user=user
            )

            return HttpResponseRedirect(reverse('mainpage'))
    else:
        form = AddUser()

    return render(request, 'generic_form.html', {'form': form})


def login_view(request):
    form = None

    if request.method == 'POST':
        form = Login(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )

            if user is not None:
                login(request, user)

                return HttpResponseRedirect(request.GET.get('next', '/'))

    else:
        form = Login()

    return render(request, 'generic_form.html', {'form': form})
