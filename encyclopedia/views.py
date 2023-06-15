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
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        with open(f"entries/{title}.md", "w") as f:
            f.write(content)
        return redirect("entry", entry=title)
    else:
        return render(request, "encyclopedia/new.html")

def entry(request, entry):
    filename = f"entries/{entry}.md"
    if os.path.exists(filename):
        with open(filename) as f:
            content = f.read()
        html = markdown(content)
        return render(request, "encyclopedia/entry.html", {"content": html})
    else:
        return render(request, "encyclopedia/error.html", {"message": f"Sorry, the requested page '{entry}' was not found."})

def search(request):
    query = request.GET.get("q")
    if not query:
        return render(request, "encyclopedia/error.html", {"message": "No search query entered."})
    entries = os.listdir("entries")
    entries = [entry.replace(".md", "") for entry in entries]
    results = []
    for entry in entries:
        if re.search(query, entry, re.IGNORECASE):
            with open(f"entries/{entry}.md") as f:
                content = f.read()
            html = markdown(content)
            results.append((entry, html))
    if not results:
        return render(request, "encyclopedia/elaborate.html", {"message": mark_safe( f"No results found for '<b>{query}</b>'. Please elaborate.")})
    return render(request, "encyclopedia/search.html", {"results": results})

