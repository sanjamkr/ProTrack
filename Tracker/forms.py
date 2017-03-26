from django.forms import ModelForm
from django import forms
from .models import project,sprint,task,tag,comment
from django.forms.extras.widgets import SelectDateWidget
import datetime


class ProfileImageForm(forms.Form):
    image = forms.FileField(label='Select a profile Image')

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
