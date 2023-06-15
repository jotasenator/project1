from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random, name="random"),
    path("new", views.new, name="new"),

    path("wiki/<str:entry>", views.entry, name="entry"),
]
