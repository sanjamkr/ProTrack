from django.contrib import admin

from .models import Task,Tags,Comment,SubTasks

admin.site.register(Task)
admin.site.register(Tags)
admin.site.register(Comment)
admin.site.register(SubTasks)
