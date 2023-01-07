from django.http import HttpResponse
from django.shortcuts import render

from . import models


def home(request):
    return render(request, 'todo/index.html')

def new_todo(request):
    if request.method == 'POST':
        
        todo_item = request.POST.get('item')
        # item = str(todo_item).strip()

        status = request.POST.get('status')
        
        if todo_item:
            if not status: status = False
            else: status = True
                
            new_item = models.Todo.objects.create(
                                    todo_item=todo_item,
                                    status=status
                                    )
            new_item.save()

            
            return HttpResponse("New Item Added!!")
        else:
            print("Wrong todo item")

    return render(request, 'todo/new_todo.html')
