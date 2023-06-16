from django.shortcuts import render

import os
import random as rnd
from django.shortcuts import redirect

from markdown2 import markdown

import re

from django.utils.safestring import mark_safe


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def random(request):
    entries = os.listdir("entries")
    entries = [entry.replace(".md", "") for entry in entries]
    entry = rnd.choice(entries)
    return redirect("entry", entry=entry)

def new(request):

    error=None
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        # Check entry with the same title already exists
        filename = f"entries/{title}.md"
        if os.path.exists(filename):
            # return render(request, "encyclopedia/error.html", {"message": f"An entry with the title '{title}' already exists."})
            error = f"An entry with the title '{title}' already exists."
        else:
            with open(filename, "w") as f:
                f.write(content)
            return redirect("entry", entry=title)   
    return render(request, "encyclopedia/new.html",{"error":error})

def entry(request, entry):
    filename = f"entries/{entry}.md"
    if os.path.exists(filename):
        with open(filename) as f:
            content = f.read()
        html = markdown(content)
        return render(request, "encyclopedia/entry.html", {"entry":entry,"content": html})
    else:
        return render(request, "encyclopedia/error.html", {"message": f"Sorry, the requested page '{entry}' was not found."})

def search(request):
    query = request.GET.get("q")
    if not query:
        return render(request, "encyclopedia/error.html", {"message": "No search query entered."})
    entries = os.listdir("entries")
    entries = [entry.replace(".md", "") for entry in entries]
    
    # Check if query matches the name of an entry exactly
    if query in entries:
        return redirect("entry", entry=query)
    
    # Search for entries that have the query as a substring
    results = []
    for entry in entries:
        if re.search(query, entry, re.IGNORECASE):
            with open(f"entries/{entry}.md") as f:
                content = f.read()
            html = markdown(content)
            results.append((entry, html))
    if not results:
        return render(request, "encyclopedia/elaborate.html", {"message": mark_safe( f"No results found for '<b>{query}</b>'. Please elaborate")})
    return render(request, "encyclopedia/search.html", {"results": results})

def edit(request, entry):
    filename = f"entries/{entry}.md"
    if request.method == "POST":
        content = request.POST["content"]
        with open(filename, "w") as f:
            f.write(content)
        return redirect("entry", entry=entry)
    else:
        if os.path.exists(filename):
            with open(filename) as f:
                content = f.read()
            return render(request, "encyclopedia/edit.html", {"entry": entry, "content": content})
        else:
            return render(request, "encyclopedia/error.html", {"message": f"Sorry, the requested page '{entry}' was not found."})

def delete(request, entry):
    filename = f"entries/{entry}.md"
    if os.path.exists(filename):
        os.remove(filename)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "encyclopedia/error.html", {"message": f"Sorry, the requested page '{entry}' was not found."})

