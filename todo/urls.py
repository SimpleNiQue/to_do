
from django.urls import path, include
from . import views


app_name = 'todo'
urlpatterns = [
    path('', views.home, name='home'),
    path('new-todo/', views.new_todo, name='new'),
    path('view-todos', views.new_todo, name='todos'),
]
