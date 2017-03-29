from django.contrib import admin
from .models import project,sprint,task,tag,comment,project_file,notification

class projectAdmin(admin.ModelAdmin):
	list_display = ('id','pname','pgroup','pcreated','pdeadline')
admin.site.register(project,projectAdmin)

class sprintAdmin(admin.ModelAdmin):
        list_display = ('id','sname','start_date','end_date')
admin.site.register(sprint,sprintAdmin)

class taskAdmin(admin.ModelAdmin):
	list_display = ('id','tname','tproject','tsprint','due_date','state','assign','tp','created','comp_time')
admin.site.register(task,taskAdmin)

class tagAdmin(admin.ModelAdmin):
        list_display = ('id','tag','task')
admin.site.register(tag,tagAdmin)

class commentAdmin(admin.ModelAdmin):
        list_display = ('id','task','comment','member','ccreated')
admin.site.register(comment,commentAdmin)

class notificationAdmin(admin.ModelAdmin):
        list_display = ('id','type','member','othermember','membergroup','urlid','content','noti_create','read','noti_date','noti_create')
admin.site.register(notification,notificationAdmin)

admin.site.register(project_file)
