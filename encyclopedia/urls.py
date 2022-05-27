from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.display_entry, name="display_entry"),
    path("search_res", views.search_res, name="search_res"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("edit/<str:entry>", views.edit, name="edit_page")
]
