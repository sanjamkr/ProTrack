from django.forms import ModelForm
from django import forms
from .models import group,member,project,sprint,task,tag,comment

class NewGroup(ModelForm):
    class Meta:
        model = group
        fields = ['gname']

class NewMember(ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = member
        fields = ['fname','lname','email','username','password','mgroup']
        
class NewProject(ModelForm):
    class Meta:
        model = project
        fields = ['pgroup','pname','pdesc','pdeadline']

class NewSprint(ModelForm):
    class Meta:
        model = sprint
        fields = ['project','sname','start_date','end_date','status']

class NewTask(ModelForm):
    class Meta:
        model = task
        fields = ['tsprint','tproject','tname','desc','due_date','risk','status','priority',
                  'state','assign','remainder','heading','dep_task','tp']
'''
        def __init__(self, *args, **kwargs):
            super(NewTask, self).__init__(*args, **kwargs)
            #if self.instance:
            self.fields['tsprint'].queryset = sprint.objects.filter(project__id=request.tproject.id)
'''
'''    def __init__(self, *args, **kwargs):
        super (NewTask,self ).__init__(project,*args,**kwargs)
        self.fields['tsprint'].queryset = sprint.objects.filter(project=task.tproject)
'''
class NewTag(ModelForm):
	class Meta:
		model = tag
		fields = ['task','tag']

class NewComment(ModelForm):
    class Meta:
        model = comment
        fields = ['task','comment']
