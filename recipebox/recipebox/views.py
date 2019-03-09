from django.shortcuts import render
from recipebox.models import Recipe, Author
from recipebox.forms import AddRecipe
from recipebox.forms import AddAuthor


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
