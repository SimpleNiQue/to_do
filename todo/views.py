from django.http import HttpResponse
from django.shortcuts import render

from . import models


def home(request):
    return render(request, 'todo/index.html')

def new_todo(request):
    if request.method == 'POST':
        print(request.POST)
        todo_item = request.POST.get('item')
        # item = str(todo_item).strip()

        status = request.POST.get('status', False)
        if status:
            status = True
        print(status)
        
        if todo_item:
                
            new_item = models.Todo.objects.create(
                                    todo_item=todo_item,
                                    status=status
                                    )
            new_item.save()

            
            return HttpResponse("New Item Added!!")
        else:
            print("Wrong todo item")

    return render(request, 'todo/new_todo.html')

def view_todo(request):
    todos = models.Todo.objects.all()
    template = 'todo/view_todo.html'
    context = {
        'all_todo': todos,
    }

    return render(request, template, context)


