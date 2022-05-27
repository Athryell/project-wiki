import random

from django.shortcuts import render
from . import util

from .forms import SearchForms, NewEntryForm, EditForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import markdown2


def index(request):
    request.session["entries_list"] = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": request.session["entries_list"],
        "search_form": SearchForms(),
        "random_page": random.choice(util.list_entries()),
    })


def display_entry(request, entry):
    if entry.capitalize() in util.list_entries():
        return render(request, "encyclopedia/display_entry.html", {
            "random_page": random.choice(util.list_entries()),
            "entry": entry.capitalize(),
            "text_file": markdown2.markdown(util.get_entry(entry)),
            "search_form": SearchForms()
        })


def edit(request, entry):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            title = entry.capitalize()
            text = (form.cleaned_data["text"]).capitalize()
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("display_entry", args=[title]))
    form = EditForm(initial={'text': util.get_entry(entry)})
    return render(request, "encyclopedia/edit_page.html", {
        "edit_form": form,
        "entry": entry,
        "random_page": random.choice(util.list_entries()),
        "md_file": markdown2.markdown(util.get_entry(entry)),
        "search_form": SearchForms()
    })


def search_res(request):
    results = []
    if request.method == "POST":
        form = SearchForms(request.POST)
        if form.is_valid():
            word = (form.cleaned_data["search"]).lower()
            for entry in util.list_entries():
                if word == entry.lower():
                    return HttpResponseRedirect(reverse("display_entry", args=[word.capitalize()]))
                if word in entry.lower():
                    results.append(entry)
            return render(request, "encyclopedia/search_res.html", {
                "results": results,
                "search_form": form,
                "random_page": random.choice(util.list_entries())
            })
    return render(request, "encyclopedia/search_res.html", {
        "results": results,
        "search_form": SearchForms(),
        "random_page": random.choice(util.list_entries()),
    })


def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = (form.cleaned_data["title"]).capitalize()
            text = (form.cleaned_data["text"]).capitalize()
            if title in util.list_entries():
                messages.warning(request, f'An entry for "{title}" already exists!')
                return render(request, "encyclopedia/new_entry.html", {
                    "random_page": random.choice(util.list_entries()),
                    "search_form": SearchForms(),
                    "new_form": form
                })
            else:
                util.save_entry(title, text)
                return HttpResponseRedirect(reverse("display_entry", args=[title]))
        else:
            return render(request, "encyclopedia/new_entry.html", {
                "random_page": random.choice(util.list_entries()),
                "search_form": SearchForms(),
                "new_form": form,
            })

    return render(request, "encyclopedia/new_entry.html", {
        "random_page": random.choice(util.list_entries()),
        "search_form": SearchForms(),
        "new_form": NewEntryForm()
    })
