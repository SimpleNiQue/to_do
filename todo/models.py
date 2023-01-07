from django.db import models


class Todo(models.Model):
    todo_item = models.CharField(max_length=120)
    status = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)



