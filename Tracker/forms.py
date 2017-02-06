from django.forms import ModelForm
from django import forms
from .models import sprint,group,project,task

class NewGroup(ModelForm):
    class Meta:
        model = group
        fields = ['gname']

class NewProject(ModelForm):
    class Meta:
        model = project
        fields = ['pgroup','pname','pdesc']

class NewTask(ModelForm):
    class Meta:
        model = task
        fields = ['project','tname','desc','risk','status','priority',
                  'state','assign','remainder','heading','dep_task','cur_sprint','tp']
        widgets = {'due_date': forms.DateInput(attrs={'class': 'datepicker'})}

class NewSprint(ModelForm):
    class Meta:
        model = sprint
        fields = ['project','sname','start_date','end_date']

