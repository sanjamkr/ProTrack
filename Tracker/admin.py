from django.contrib import admin

from .models import member,group,group_member,project,task,tag,comment,subtask,sprint

# Register your models here.

admin.site.register(member)
admin.site.register(group)
admin.site.register(group_member)
# admin.site.register(project)
class projectAdmin(admin.ModelAdmin):
	list_display = ('pname','pgroup')
# admin.site.register(task)
class taskAdmin(admin.ModelAdmin):
	list_display = ('tname','project', 'due_date', 'status','priority')
	list_filter = ('due_date','status')
admin.site.register(task,taskAdmin)
admin.site.register(project,projectAdmin)
admin.site.register(tag)
admin.site.register(comment)
admin.site.register(subtask)
class sprintAdmin(admin.ModelAdmin):
        list_display = ('id','sname')
admin.site.register(sprint,sprintAdmin)
