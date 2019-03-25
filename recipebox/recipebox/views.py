from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from recipebox.models import Recipe, Author, Favorite
from recipebox.forms import AddRecipe, AddAuthor, AddUser, Login


def mainpage(request):
    recipes = Recipe.objects.all()

    return render(request, 'mainpage.html', {'data': recipes})


def recipe(request, r_id):
    recipe = Recipe.objects.filter(id=r_id).first()

    if(request.method == 'GET'
       and request.GET.get('favorite')
       and request.user.is_authenticated):
        Favorite.objects.create(
            recipe=recipe,
            user=request.user)

    return render(request, 'recipe.html', {'data': recipe})


def author(request, a_id):
    author = Author.objects.filter(id=a_id).first()
    recipes = Recipe.objects.filter(author=a_id)
    favorites = Favorite.objects.filter(user=author.user)

    return render(request, 'author.html', {
        'a_data': author, 'r_data': recipes, 'f_data': favorites})


@login_required
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


@login_required
def editrecipe(request, r_id):
    form = None
    recipe = Recipe.objects.filter(id=r_id).first()

    if request.method == 'POST':
        form = AddRecipe(request.POST)

        if(form.is_valid() and request.user.id is recipe.author.user.id
           or request.user.is_staff):
            data = form.cleaned_data
            Recipe.objects.filter(id=r_id).update(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                time_req=data['time_req'],
                instructions=data['instructions']
            )

            return render(request, 'success.html')

    elif(request.user.is_authenticated
         and request.user.id is recipe.author.user.id
         or request.user.is_staff):

        recipe = Recipe.objects.get(id=r_id)
        form = AddRecipe(initial={
            'title': recipe.title,
            'author': recipe.author,
            'description': recipe.description,
            'time_req': recipe.time_req,
            'instructions': recipe.instructions,
        })
    else:
        reverse('/')

    return render(request, 'generic_form.html', {'form': form})


@login_required
def deleterecipe(request, r_id):
    recipe = Recipe.objects.get(id=r_id)
    if(request.method == 'GET' and request.user.id is recipe.author.user.id
       or request.user.is_staff):
        (code, items) = recipe.delete()
        return render(request, 'success.html')
    else:
        return reverse('mainpage')


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
