from django.http import HttpResponse
from django.shortcuts import render

from . import models


def home(request):
    return render(request, 'todo/index.html')

def new_todo(request):
    if request.method == 'POST':
        
        todo_item = request.POST['item']
        todo_item = str(todo_item).strip()

        status = request.POST['status']

        if todo_item:
            models.Todo.objects.create(
                                    todo_item=todo_item,
                                    status=status
                                    )
            return HttpResponse("New Item Added!!")
        else:
            print("Wrong todo item")

    return render(request, 'todo/new_todo.html')
