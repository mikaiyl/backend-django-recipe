from django import forms
from django.contrib.auth.models import User
from recipebox.models import Author


class AddRecipe(forms.Form):
    title = forms.CharField(max_length=40)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(max_length=100)
    time_req = forms.IntegerField()
    instructions = forms.CharField(widget=forms.Textarea)


class AddAuthor(forms.Form):
    name = forms.CharField(max_length=40)
    user = forms.ModelChoiceField(queryset=User.objects.all())
    bio = forms.CharField(widget=forms.Textarea)


class AddUser(forms.Form):
    name = forms.CharField(max_length=40)
    username = forms.CharField(max_length=40)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class Login(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(widget=forms.PasswordInput())
