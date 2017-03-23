from django.forms import ModelForm
from django import forms
from .models import group,member,project,sprint,task,tag,comment
from django.forms.extras.widgets import SelectDateWidget
import datetime

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
    pdeadline = forms.DateField(widget=SelectDateWidget)
    class Meta:
        model = project
        fields = ['pgroup','pname','pdesc','pdeadline']

class NewSprint(ModelForm):
    start_date = forms.DateField(widget=SelectDateWidget)
    end_date = forms.DateField(widget=SelectDateWidget)
    class Meta:
        model = sprint
        fields = ['project','sname','start_date','end_date']

class NewTask(ModelForm):
    due_date = forms.DateField(widget=SelectDateWidget)
    class Meta:
        model = task
        fields = ['tsprint','tproject','tname','desc','due_date','risk','priority',
                  'state','assign','remainder','heading','dep_task','tp']

class NewTag(ModelForm):
	class Meta:
		model = tag
		fields = ['task','tag']

class NewComment(ModelForm):
    class Meta:
        model = comment
        fields = ['task','member','comment']
