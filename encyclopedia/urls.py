from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("random", views.random, name="random"),

    path("new", views.new, name="new"),

    path("wiki/<str:entry>", views.entry, name="entry"),

    path("search",views.search,name="search"),

    path("edit/<str:entry>", views.edit, name="edit"),
]
