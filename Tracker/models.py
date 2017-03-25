from django.db import models
from django.contrib.auth.models import User,Group

import datetime

#Projects associated with a Group

class project(models.Model):                                                                 
    pgroup = models.ForeignKey(Group)
    pname = models.CharField(max_length=100,verbose_name = "Project Name")
    pdesc = models.CharField(max_length=100,blank=True,verbose_name = "Project Description")
    pcreated = models.DateTimeField(auto_now_add=True,verbose_name = "Create time")
    pdeadline = models.DateTimeField('Dead Line')
    
    def __str__(self):
        return self.pname

#.................................

Priority_Choices = (
    ('high','High'),('medium','Medium'),('low','Low'),
)
State_Choices = (
    ('open','Open'),('blocked','Blocked'),('completed', 'Completed'),
)

# Sprints for a Project
class sprint(models.Model): 
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    sname = models.CharField(max_length=100,verbose_name='Sprint Name')
    start_date = models.DateField('start date')
    end_date = models.DateField('end date')
  
    def __str__(self):
        return self.sname

#Tasks associated with a Project
class task(models.Model):
    tproject = models.ForeignKey(project, on_delete=models.CASCADE)
    tsprint = models.ForeignKey(sprint, on_delete=models.CASCADE,blank=True,null=True)
    tname = models.CharField(max_length=100)
    desc = models.CharField(max_length=200,blank=True)
    due_date = models.DateField('due date')
    risk = models.CharField(max_length=200,blank=True)
    priority = models.CharField(max_length=50,choices=Priority_Choices)
    state = models.CharField(max_length=50, default='open',choices=State_Choices)
    assign =  models.ForeignKey(User,blank=True, null=True)
    remainder = models.CharField(max_length=200,blank=True)
    heading = models.CharField(max_length=200,blank=True)
    dep_task = models.CharField(max_length=100,blank=True)
    tp = models.IntegerField(default=1)
    comp_time = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tname
    
    def __init__(self, *args, **kwargs):
        super(task, self).__init__(*args, **kwargs)
        self.old_state = self.state
    
    def save(self, force_insert=False, force_update=False):
        if (self.old_state == 'open' or self.old_state=='blocked') and self.state == 'completed':
            self.comp_time = datetime.datetime.now()
        elif self.old_state == 'completed' and (self.state == 'open'  or self.state=='blocked'):
            self.comp_time = None
        super(task, self).save(force_insert, force_update)
        self.old_state = self.state
        
# Task's associated tags
class tag(models.Model):
     task = models.ForeignKey(task, on_delete=models.CASCADE)
     tag = models.CharField(max_length=100)

# Task's associated comments
class comment(models.Model):
     task = models.ForeignKey(task, on_delete=models.CASCADE)
     member = models.ForeignKey(User)
     comment = models.CharField(max_length=500)
     ccreated = models.DateTimeField(auto_now_add=True)
