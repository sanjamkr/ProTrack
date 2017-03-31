from django.forms import ModelForm
from django import forms
from .models import project,sprint,task,tag,comment,project_file
from django.forms.extras.widgets import SelectDateWidget
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'signupinput firstname','placeholder':'First Name*'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'signupinput lastname','placeholder':'Last Name'}))
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'signupinput email','placeholder':'Email ID*'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'signupinput password1','placeholder':'Password*'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'signupinput password2','placeholder':'Confirm Password*'}))



    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
        widgets = {
        'username': forms.TextInput(attrs={'class': 'signupinput username','placeholder':'Username*'}),      
        }

class NewFile(ModelForm):
     class Meta:
        model = project_file
        fields = ['fproject','file']

class NewProject(ModelForm):
    pdeadline = forms.DateField(widget=SelectDateWidget(years=range(datetime.date.today().year, datetime.date.today().year+10 )),initial = datetime.date.today())
    class Meta:
        model = project
        fields = ['pgroup','pname','pdesc','pdeadline']
        widgets = {
        'pname': forms.TextInput(attrs={'class': 'projectinput projectname'}),
        'pdesc': forms.TextInput(attrs={'class': 'projectinput projectdesc'}),
        }
class NewSprint(ModelForm):
    start_date = forms.DateField(widget=SelectDateWidget(years=range(datetime.date.today().year, datetime.date.today().year+10 )),initial = datetime.date.today())
    end_date = forms.DateField(widget=SelectDateWidget(years=range(datetime.date.today().year, datetime.date.today().year+10 )), initial = datetime.date.today()+datetime.timedelta(days=1))
    class Meta:
        model = sprint
        fields = ['project','sname','start_date','end_date']
        widgets = {
        'sname': forms.TextInput(attrs={'class': 'sprintinput sprintname'}),
        }
    def clean(self):
        cleaned_data = super(NewSprint, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if  end_date < start_date:
            raise forms.ValidationError("Sprint cannot end before starting")

class NewTask(ModelForm):
    due_date = forms.DateField(widget=SelectDateWidget(years=range(datetime.date.today().year, datetime.date.today().year+10 )), initial = datetime.date.today())
    class Meta:
        model = task
        fields = ['tsprint','tproject','tname','desc','due_date','risk','priority','state','assign','remainder','heading','dep_task','tp']
        exclude = ('newcomment','newtag',)
        widgets = {
        'tname': forms.TextInput(attrs={'class': 'taskinput taskname'}),
        'desc': forms.TextInput(attrs={'class': 'taskinput taskname'}),
        'tp': forms.NumberInput(attrs={'class': 'taskinput taskpoint'}),
        'priority': forms.TextInput(attrs={'class': 'taskinput priority'}),
        'heading': forms.TextInput(attrs={'class': 'taskinput heading'}),
        'dep_task': forms.TextInput(attrs={'class': 'taskinput dep_task'}),
        'remainder': forms.TextInput(attrs={'class': 'taskinput remainder'}),
        'risk': forms.TextInput(attrs={'class': 'taskinput risk'}),

        }        

class NewComment(ModelForm):
    class Meta:
        model = comment
        fields = ['task','member','comment']
        exclude = ('newtask','newtag',)
        widgets = {
            'comment': forms.TextInput(attrs={'class': 'commentbox','placeholder':'Write a comment...'}),
        }
        
class NewTag(ModelForm):
    class Meta:
        model = tag
        fields = ['task','tag']
        exclude = ('newcomment','newtask',)
        widgets = {
            'tag': forms.TextInput(attrs={'class': 'tagbox','placeholder':'Add a Tag...'}),
        }
