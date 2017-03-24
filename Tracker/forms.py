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
        
        '''def __init__(self, *args, **kwargs):
            super(NewProject, self).__init__(*args, **kwargs)
            self.__old_pdeadline = self.pdeadline
            
        def clean(self):
            " Make sure expiry time cannot be in the past "
            if (self.__old_pdeadline != self.pdeadline) and self.pdeadline < timezone.now():
                raise ValidationError('Deadline cannot be a date in the past')'''

class NewSprint(ModelForm):
    start_date = forms.DateField(widget=SelectDateWidget)
    end_date = forms.DateField(widget=SelectDateWidget)
    class Meta:
        model = sprint
        fields = ['project','sname','start_date','end_date']
    def clean(self):
        cleaned_data = super(NewSprint, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if  end_date < start_date:
            raise forms.ValidationError("Sprint cannot end before starting")

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
