from django.forms import ModelForm
from django import forms
from .models import group,member,project,sprint,task,tag,comment

class NewGroup(ModelForm):
    class Meta:
        model = group
        fields = ['gname']

class NewMember(ModelForm):
    class Meta:
        model = member
        fields = ['fname','lname','email','username','password','mgroup']

class NewProject(ModelForm):
    class Meta:
        model = project
        fields = ['pgroup','pname','pdesc']

class NewSprint(ModelForm):
    class Meta:
        model = sprint
        fields = ['project','sname','start_date','end_date','status']

class NewTask(ModelForm):
    class Meta:
        model = task
        fields = ['tsprint','tproject','tname','desc','due_date','risk','status','priority',
                  'state','assign','remainder','heading','dep_task','tp']

class NewTag(ModelForm):
	class Meta:
		model = tag
		fields = ['task','tag']

class NewComment(ModelForm):
    class Meta:
        model = comment
        fields = ['task','comment']
