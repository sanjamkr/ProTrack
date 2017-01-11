from django.contrib import admin

from .models import member,group,group_member,project,task,tag,comment,subtask,sprint,sprint_task

# Register your models here.

admin.site.register(member)
admin.site.register(group)
admin.site.register(group_member)
admin.site.register(project)
admin.site.register(task)
admin.site.register(tag)
admin.site.register(comment)
admin.site.register(subtask)
admin.site.register(sprint)
admin.site.register(sprint_task)
