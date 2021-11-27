from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("new_page", views.new_page, name="new_page"),
    path("wiki/<str:name>/edit", views.edit, name="edit"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("error", views.error, name="error"),
    path("search", views.search, name="search")
]
