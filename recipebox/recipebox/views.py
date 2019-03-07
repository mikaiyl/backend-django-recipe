from django.shortcuts import render
from recipebox.models import Recipe
from recipebox.models import Author


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
