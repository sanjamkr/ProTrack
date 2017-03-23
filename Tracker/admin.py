from django.contrib import admin
from .models import group,member,project,sprint,task,tag,comment

admin.site.register(group)

admin.site.register(member)

class projectAdmin(admin.ModelAdmin):
	list_display = ('id','pname','pgroup')
admin.site.register(project,projectAdmin)

class sprintAdmin(admin.ModelAdmin):
        list_display = ('id','sname')
admin.site.register(sprint,sprintAdmin)

class taskAdmin(admin.ModelAdmin):
	list_display = ('id','tname','tproject', 'due_date','priority')
admin.site.register(task,taskAdmin)

admin.site.register(tag)

admin.site.register(comment)
