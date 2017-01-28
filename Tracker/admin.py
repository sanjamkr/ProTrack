from django.contrib import admin

# Register your models here.
from .models import member,group,project,task,tag,comment,subtask,sprint

admin.site.register(member)
admin.site.register(group)
class projectAdmin(admin.ModelAdmin):
	list_display = ('pname','pgroup')
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
