from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django import forms
from django.urls import reverse
from markdown2 import Markdown
import random

from . import util
markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random_page" : random.choice(util.list_entries())
    })

def error(request):
    return render(request, "encyclopedia/error.html")

def entry(request, name):
    if name in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "name" : name,  
            "contents" : markdowner.convert(util.get_entry(name)),
            "random_page" : random.choice(util.list_entries())
        })
    else:
        return redirect("error")

def new_page(request):

    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            contents = form.cleaned_data["contents"]
            if title not in util.list_entries():
                with open('entries/' + title + '.md', 'w') as file:
                    file.write(contents)
                return redirect("wiki/" + title)
            else:
                messages.error(request, "There is already a page with the name " + title)
                return render(request, "encyclopedia/new_page.html", {
                    "random_page" : random.choice(util.list_entries()),
                    "form" : form
                })
                
    return render(request, "encyclopedia/new_page.html", {
        "random_page" : random.choice(util.list_entries()),
        "form" : NewPageForm()
    })

def edit(request, name):
    
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            contents = form.cleaned_data["contents"]
            with open('entries/' + name + '.md', 'w') as file:
                file.write(contents)
            return redirect("entry", name=name)
                
    return render(request, "encyclopedia/edit.html", {
        "random_page" : random.choice(util.list_entries()),
        "name" : name,
        "contents" : util.get_entry(name)
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                return redirect("entry", name=title)
            else:
                return render(request, "encyclopedia/search.html", {
                    "search_term" : title,
                    "entries" : util.list_entries()
                })

    return render(request, "encyclopedia/search.html", {
        "search_term" : "",
        "entries" : util.list_entries()
    })


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title of new page:", widget=forms.TextInput(attrs={"class":"titlebox", "placeholder":"type in the title"}))
    contents = forms.CharField(label="", widget=forms.Textarea(attrs={"class":"contentsbox", "placeholder":"type in the contents"}))

class EditPageForm(forms.Form):
    contents = forms.CharField()

class SearchForm(forms.Form):
    title = forms.CharField()
