from django.contrib import admin
from .models import group,member,project,sprint,task,tag,comment

admin.site.register(group)

admin.site.register(member)

class projectAdmin(admin.ModelAdmin):
	list_display = ('pname','pgroup')
admin.site.register(project,projectAdmin)

class sprintAdmin(admin.ModelAdmin):
        list_display = ('id','sname')
admin.site.register(sprint,sprintAdmin)

class taskAdmin(admin.ModelAdmin):
	list_display = ('tname','tproject', 'due_date', 'status','priority')
	list_filter = ('due_date','status')
admin.site.register(task,taskAdmin)

admin.site.register(tag)

admin.site.register(comment)
