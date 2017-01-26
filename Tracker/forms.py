from django.forms import ModelForm
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
        fields = ['project','tname','desc','due_date','risk','status','priority',
                  'state','assign','remainder','heading','dep_task','cur_sprint','tp']

class NewSprint(ModelForm):
    class Meta:
        model = sprint
        fields = ['project','sname','start_date','end_date']
    #sname = forms.CharField(label='Sprint Name', max_length=100)
    #project = forms.ChoiceField(project, on_delete=models.CASCADE)
    #start_date = forms.DateField(label='Start Date')
    #end_date = forms.DateField(label='End Date')

#form = NewSprint()

# Creating a form to change an existing article.
#sprint = sprint.objects.get(pk=1)
#form = NewSprint(instance=article)

