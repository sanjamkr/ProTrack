
from django.db import models

class Task(models.Model):
    tname = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    due_date =models.DateField('due date')
    risk = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    assign = models.CharField(max_length=100)
    remainder = models.CharField(max_length=200)
    heading = models.CharField(max_length=200)
    dep_task = models.CharField(max_length=100)
    tp = models.IntegerField(default=1)

    def __str__(self):
        return self.tname

class Tags(models.Model):
     task = models.ForeignKey(Task, on_delete=models.CASCADE)
     tag = models.CharField(max_length=100)
     def __str__(self):
        return self.tag

class Comment(models.Model):
     task = models.ForeignKey(Task, on_delete=models.CASCADE)
     comment = models.CharField(max_length=500)
     def __str__(self):
        return self.comment

class SubTasks(models.Model):
     task = models.ForeignKey(Task, on_delete=models.CASCADE)
     subtask = models.CharField(max_length=500)
     def __str__(self):
        return self.subtask
