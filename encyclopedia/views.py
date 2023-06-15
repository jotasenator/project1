from django.shortcuts import render
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def new(request):
    return render(request, "encyclopedia/new.html")
    
def random(request):
    return render(request, "encyclopedia/random.html")



def entry(request, entry):
    with open(f"entries/{entry}.md") as f:
        content = f.read()
    html = markdown(content)
    return render(request, "encyclopedia/entry.html", {"content": html})

